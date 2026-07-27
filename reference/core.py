from __future__ import annotations

import base64
import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest(value: Any) -> str:
    raw = value if isinstance(value, bytes) else canonical(value)
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


@dataclass
class ApprovalStore:
    approvals: dict[str, dict[str, Any]] = field(default_factory=dict)
    consumed: set[str] = field(default_factory=set)

    def issue(self, reference: str, binding: dict[str, Any]) -> None:
        self.approvals[reference] = binding

    def consume(self, reference: str, envelope: dict[str, Any]) -> bool:
        if reference in self.consumed:
            return False
        binding = self.approvals.get(reference)
        if not binding:
            return False
        keys = ("agent_identity", "capability_id", "tenant", "environment", "payload_hash")
        if any(binding.get(key) != envelope.get(key) for key in keys):
            return False
        if binding.get("resource_scope") != envelope.get("resource_scope"):
            return False
        self.consumed.add(reference)
        return True


@dataclass
class ReferencePEP:
    private_key: Ed25519PrivateKey
    key_id: str
    delegated_capabilities: set[str]
    approval_store: ApprovalStore = field(default_factory=ApprovalStore)
    previous_record_hash: str | None = None
    outcomes: dict[str, tuple[str, dict[str, Any]]] = field(default_factory=dict)

    def evaluate(self, envelope: dict[str, Any]) -> tuple[str, str]:
        capability = envelope["capability_id"]
        if capability not in self.delegated_capabilities:
            return "DENY", "undelegated_capability"
        if capability == "repository.merge.production":
            ref = envelope.get("approval_reference")
            if not ref:
                return "HOLD", "approval_required"
            if not self.approval_store.consume(ref, envelope):
                return "DENY", "invalid_or_replayed_approval"
        return "ALLOW", "policy_allow"

    def govern(
        self, envelope: dict[str, Any], executor: Callable[[], Any]
    ) -> dict[str, Any]:
        binding_hash = digest({
            "action": envelope["requested_action"],
            "payload_hash": envelope["payload_hash"],
            "scope": envelope["resource_scope"],
        })
        prior = self.outcomes.get(envelope["idempotency_key"])
        if prior:
            prior_binding, prior_receipt = prior
            if prior_binding != binding_hash:
                return self._receipt(envelope, "DENY", "idempotency_binding_mismatch", False, None)
            return prior_receipt

        decision, reason = self.evaluate(envelope)
        if decision != "ALLOW":
            receipt = self._receipt(envelope, decision, reason, False, None)
            self.outcomes[envelope["idempotency_key"]] = (binding_hash, receipt)
            return receipt

        try:
            result = executor()
            receipt = self._receipt(envelope, decision, reason, True, result)
        except Exception as exc:
            receipt = self._receipt(
                envelope, decision, reason, True, None,
                error_code=type(exc).__name__,
            )
        self.outcomes[envelope["idempotency_key"]] = (binding_hash, receipt)
        return receipt

    def _receipt(
        self,
        envelope: dict[str, Any],
        decision: str,
        reason: str,
        attempted: bool,
        result: Any,
        error_code: str | None = None,
    ) -> dict[str, Any]:
        succeeded = attempted and error_code is None
        execution: dict[str, Any] = {
            "authorized": decision == "ALLOW",
            "attempted": attempted,
            "status": "SUCCEEDED" if succeeded else ("FAILED" if attempted else "NOT_ATTEMPTED"),
        }
        if succeeded:
            execution["result_hash"] = digest(result)
        if error_code:
            execution["error_code"] = error_code

        receipt: dict[str, Any] = {
            "profile_version": "0.1",
            "receipt_id": str(uuid.uuid4()),
            "issued_at": utc_now(),
            "request": envelope,
            "authority": {
                "status": "VALID",
                "subject": envelope["agent_identity"],
                "capabilities": sorted(self.delegated_capabilities),
            },
            "policy": {
                "policy_id": "demo.secure-coding",
                "policy_version": "1",
                "status": "EVALUATED",
            },
            "decision": decision,
            "execution": execution,
            "evidence_hashes": [digest({"decision_reason": reason})],
        }
        if self.previous_record_hash:
            receipt["previous_record_hash"] = self.previous_record_hash
        receipt["record_hash"] = digest(receipt)
        receipt["signature"] = {
            "algorithm": "Ed25519",
            "key_id": self.key_id,
            "value": b64url(self.private_key.sign(canonical(receipt))),
        }
        self.previous_record_hash = receipt["record_hash"]
        return receipt


def envelope(
    capability: str,
    action: str,
    payload: Any,
    scope: dict[str, Any],
    *,
    risk: str = "high",
    approval_reference: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "profile_version": "0.1",
        "request_id": str(uuid.uuid4()),
        "issued_at": utc_now(),
        "agent_identity": "spiffe://demo.example/agent/remediator",
        "capability_id": capability,
        "requested_action": action,
        "resource_scope": scope,
        "risk_level": risk,
        "tenant": "public-demo",
        "environment": "controlled",
        "payload_hash": digest(payload),
        "authority_chain": ["demo-delegation-v1"],
        "idempotency_key": idempotency_key or str(uuid.uuid4()),
    }
    if approval_reference:
        value["approval_reference"] = approval_reference
    return value

