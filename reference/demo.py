from __future__ import annotations

import base64
import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .core import ReferencePEP, envelope
from .verify import verify


def main() -> None:
    output = Path("proof-bundle")
    output.mkdir(exist_ok=True)
    key = Ed25519PrivateKey.generate()
    public_pem = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    (output / "public-key.pem").write_bytes(public_pem)
    public_raw = key.public_key().public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw,
    )
    encoded = base64.urlsafe_b64encode(public_raw).rstrip(b"=").decode("ascii")
    (output / "jwks.json").write_text(json.dumps({
        "keys": [{
            "kty": "OKP", "crv": "Ed25519", "use": "sig",
            "alg": "EdDSA", "kid": "demo-ed25519-2026-01", "x": encoded,
        }]
    }, indent=2) + "\n", encoding="utf-8")
    pep = ReferencePEP(
        key,
        "demo-ed25519-2026-01",
        {
            "repository.inspect",
            "repository.patch.propose",
            "repository.merge.production",
        },
    )
    calls: list[str] = []
    cases = [
        (
            "inspect-allowed",
            envelope("repository.inspect", "inspect repository", {"ref": "HEAD"}, {"repository": "demo/repo"}),
            lambda: calls.append("inspect") or {"finding_count": 1},
        ),
        (
            "patch-allowed",
            envelope("repository.patch.propose", "propose patch", {"patch": "sha256:demo"}, {"repository": "demo/repo", "branch": "remediation"}),
            lambda: calls.append("patch") or {"branch": "remediation"},
        ),
        (
            "merge-held",
            envelope("repository.merge.production", "merge to production", {"commit": "abc123"}, {"repository": "demo/repo", "branch": "main"}, risk="critical"),
            lambda: calls.append("merge") or {"merged": True},
        ),
        (
            "credential-rotation-denied",
            envelope("credentials.rotate", "rotate production credential", {"credential": "prod-api"}, {"vault": "production"}, risk="critical"),
            lambda: calls.append("rotate") or {"rotated": True},
        ),
    ]
    predecessor = None
    report = []
    for name, request, executor in cases:
        receipt = pep.govern(request, executor)
        path = output / f"receipt-{name}.json"
        path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        result = verify(receipt, public_pem, predecessor)
        report.append({"case": name, "decision": receipt["decision"], "verification": result})
        predecessor = receipt
    (output / "verification-report.json").write_text(
        json.dumps({"executor_calls": calls, "cases": report}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"executor_calls": calls, "cases": report}, indent=2))


if __name__ == "__main__":
    main()
