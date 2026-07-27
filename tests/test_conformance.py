from __future__ import annotations

import copy
import json
import unittest

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from reference.core import ApprovalStore, ReferencePEP, canonical, envelope
from reference.verify import verify


class ConformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = Ed25519PrivateKey.generate()
        self.public = self.key.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        self.pep = ReferencePEP(
            self.key,
            "test-key",
            {"repository.inspect", "repository.merge.production"},
            ApprovalStore(),
        )

    def test_allowed_action_executes_once(self) -> None:
        calls = []
        request = envelope("repository.inspect", "inspect", {}, {"repository": "demo"}, idempotency_key="same-key-00000001")
        first = self.pep.govern(request, lambda: calls.append(1) or {"ok": True})
        second = self.pep.govern(request, lambda: calls.append(2) or {"ok": True})
        self.assertEqual([1], calls)
        self.assertEqual(first["receipt_id"], second["receipt_id"])

    def test_held_action_does_not_execute(self) -> None:
        calls = []
        request = envelope("repository.merge.production", "merge", {}, {"repository": "demo"})
        receipt = self.pep.govern(request, lambda: calls.append(1))
        self.assertEqual("HOLD", receipt["decision"])
        self.assertEqual([], calls)

    def test_undelegated_action_is_denied(self) -> None:
        calls = []
        request = envelope("credentials.rotate", "rotate", {}, {"vault": "prod"})
        receipt = self.pep.govern(request, lambda: calls.append(1))
        self.assertEqual("DENY", receipt["decision"])
        self.assertEqual([], calls)
        self.assertTrue(verify(receipt, self.public)["valid"])

    def test_approval_is_single_use_and_scope_bound(self) -> None:
        ref = "approval-reference-0001"
        request = envelope(
            "repository.merge.production", "merge", {"commit": "a"},
            {"repository": "demo"}, approval_reference=ref,
        )
        binding = {key: request[key] for key in (
            "agent_identity", "capability_id", "tenant", "environment",
            "payload_hash", "resource_scope",
        )}
        self.pep.approval_store.issue(ref, binding)
        first = self.pep.govern(request, lambda: {"merged": True})
        replay = copy.deepcopy(request)
        replay["request_id"] = "3ecbfa3e-82f4-4324-879f-75d13f60d07b"
        replay["idempotency_key"] = "different-key-000001"
        second = self.pep.govern(replay, lambda: {"merged": True})
        self.assertEqual("ALLOW", first["decision"])
        self.assertEqual("DENY", second["decision"])

    def test_tampered_receipt_fails_verification(self) -> None:
        request = envelope("repository.inspect", "inspect", {}, {"repository": "demo"})
        receipt = self.pep.govern(request, lambda: {"ok": True})
        receipt["decision"] = "DENY"
        self.assertFalse(verify(receipt, self.public)["valid"])

    def test_wrong_key_fails_verification(self) -> None:
        request = envelope("repository.inspect", "inspect", {}, {"repository": "demo"})
        receipt = self.pep.govern(request, lambda: {"ok": True})
        wrong = Ed25519PrivateKey.generate().public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        self.assertFalse(verify(receipt, wrong)["valid"])

    def test_unknown_key_id_fails_with_keyset(self) -> None:
        request = envelope("repository.inspect", "inspect", {}, {"repository": "demo"})
        receipt = self.pep.govern(request, lambda: {"ok": True})
        self.assertFalse(verify(receipt, {})["valid"])

    def test_wrong_algorithm_fails_verification(self) -> None:
        request = envelope("repository.inspect", "inspect", {}, {"repository": "demo"})
        receipt = self.pep.govern(request, lambda: {"ok": True})
        receipt["signature"]["algorithm"] = "RS256"
        self.assertFalse(verify(receipt, self.public)["valid"])

    def test_missing_signature_fails_verification(self) -> None:
        request = envelope("repository.inspect", "inspect", {}, {"repository": "demo"})
        receipt = self.pep.govern(request, lambda: {"ok": True})
        del receipt["signature"]
        self.assertFalse(verify(receipt, self.public)["valid"])

    def test_malformed_key_fails_verification(self) -> None:
        request = envelope("repository.inspect", "inspect", {}, {"repository": "demo"})
        receipt = self.pep.govern(request, lambda: {"ok": True})
        self.assertFalse(verify(receipt, b"not a public key")["valid"])

    def test_mixed_profile_version_fails_verification(self) -> None:
        request = envelope("repository.inspect", "inspect", {}, {"repository": "demo"})
        receipt = self.pep.govern(request, lambda: {"ok": True})
        receipt["profile_version"] = "0.0"
        self.assertFalse(verify(receipt, self.public)["valid"])

    def test_canonicalization_is_key_order_independent(self) -> None:
        left = {"z": 1, "a": {"y": 2, "b": 3}}
        right = json.loads('{"a":{"b":3,"y":2},"z":1}')
        self.assertEqual(canonical(left), canonical(right))

    def test_executor_failure_is_signed(self) -> None:
        request = envelope("repository.inspect", "inspect", {}, {"repository": "demo"})
        def fail() -> None:
            raise TimeoutError("executor timed out")
        receipt = self.pep.govern(request, fail)
        self.assertEqual("FAILED", receipt["execution"]["status"])
        self.assertEqual("TimeoutError", receipt["execution"]["error_code"])
        self.assertTrue(verify(receipt, self.public)["valid"])

    def test_historical_receipt_verifies_after_rotation(self) -> None:
        old_request = envelope("repository.inspect", "inspect", {}, {"repository": "demo"})
        old_receipt = self.pep.govern(old_request, lambda: {"ok": True})
        new_key = Ed25519PrivateKey.generate()
        trust = {
            "test-key": self.key.public_key(),
            "rotated-key": new_key.public_key(),
        }
        self.assertTrue(verify(old_receipt, trust)["valid"])

    def test_idempotency_key_rebinding_is_denied(self) -> None:
        key = "binding-key-0000001"
        first = envelope("repository.inspect", "inspect", {"ref": "a"}, {"repository": "demo"}, idempotency_key=key)
        second = envelope("repository.inspect", "inspect", {"ref": "b"}, {"repository": "demo"}, idempotency_key=key)
        self.pep.govern(first, lambda: {"ok": True})
        receipt = self.pep.govern(second, lambda: {"should_not": "execute"})
        self.assertEqual("DENY", receipt["decision"])

    def test_unsigned_legacy_receipt_is_not_accepted(self) -> None:
        legacy = {
            "profile_version": "legacy",
            "decision": "ALLOW",
            "execution": {"authorized": True, "attempted": True, "status": "SUCCEEDED"},
        }
        self.assertFalse(verify(legacy, self.public)["valid"])


if __name__ == "__main__":
    unittest.main()
