from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .core import canonical


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def load_jwks(raw: bytes) -> dict[str, Ed25519PublicKey]:
    data = json.loads(raw)
    result = {}
    for item in data.get("keys", []):
        if item.get("kty") == "OKP" and item.get("crv") == "Ed25519":
            result[item["kid"]] = Ed25519PublicKey.from_public_bytes(_decode(item["x"]))
    return result


def verify(
    receipt: dict[str, Any],
    trust: bytes | dict[str, Ed25519PublicKey],
    predecessor: dict[str, Any] | None = None,
) -> dict[str, Any]:
    findings: dict[str, bool] = {}
    findings["profile_version"] = receipt.get("profile_version") == "0.1"

    unsigned = dict(receipt)
    signature = unsigned.pop("signature", {})
    hash_input = dict(unsigned)
    stored_hash = hash_input.pop("record_hash", "")
    computed_hash = "sha256:" + hashlib.sha256(canonical(hash_input)).hexdigest()
    findings["record_hash"] = hmac.compare_digest(stored_hash, computed_hash)

    try:
        if isinstance(trust, dict):
            key = trust[signature["key_id"]]
        else:
            key = serialization.load_pem_public_key(trust)
        key.verify(_decode(signature["value"]), canonical(unsigned))
        findings["signature"] = (
            signature.get("algorithm") == "Ed25519"
            and bool(signature.get("key_id"))
        )
    except (ValueError, KeyError, TypeError, InvalidSignature):
        findings["signature"] = False

    request = receipt.get("request", {})
    authority = receipt.get("authority", {})
    authority_base = (
        authority.get("status") == "VALID"
        and authority.get("subject") == request.get("agent_identity")
    )
    has_capability = request.get("capability_id") in authority.get("capabilities", [])
    decision = receipt.get("decision")
    findings["authority_binding"] = (
        authority_base
        and (has_capability if decision in ("ALLOW", "HOLD") else True)
    )
    findings["policy"] = receipt.get("policy", {}).get("status") == "EVALUATED"

    execution = receipt.get("execution", {})
    if decision in ("HOLD", "DENY"):
        findings["execution_consistency"] = (
            execution.get("authorized") is False
            and execution.get("attempted") is False
            and execution.get("status") == "NOT_ATTEMPTED"
        )
    else:
        findings["execution_consistency"] = (
            decision == "ALLOW"
            and execution.get("authorized") is True
            and (
                execution.get("status") != "SUCCEEDED"
                or bool(execution.get("result_hash"))
            )
        )

    if predecessor is None:
        findings["chain"] = "previous_record_hash" not in receipt
    else:
        findings["chain"] = (
            receipt.get("previous_record_hash") == predecessor.get("record_hash")
        )
    return {"valid": all(findings.values()), "findings": findings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify an OAECP execution receipt.")
    parser.add_argument("receipt", type=Path)
    parser.add_argument("trust_bundle", type=Path, help="PEM public key or JWKS")
    parser.add_argument("--predecessor", type=Path)
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    predecessor = (
        json.loads(args.predecessor.read_text(encoding="utf-8"))
        if args.predecessor else None
    )
    trust_raw = args.trust_bundle.read_bytes()
    trust = load_jwks(trust_raw) if args.trust_bundle.suffix.lower() == ".json" else trust_raw
    result = verify(receipt, trust, predecessor)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
