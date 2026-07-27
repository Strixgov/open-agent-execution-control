# Open Agent Execution Control Profile (OAECP)

Version 0.1.0-draft

The key words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are to be interpreted as described in RFC 2119 and RFC 8174.

## 1. Purpose

OAECP defines the boundary between an agent's expressed intent and a consequential side effect. It standardizes:

1. a governed action envelope;
2. point-of-use authorization;
3. optional single-use approval consumption;
4. pre-invocation enforcement;
5. a canonical signed execution receipt;
6. independent verification.

The profile is model-neutral, harness-neutral, and policy-engine-neutral.

## 2. Roles

- **Requester**: agent or workload expressing an action.
- **Identity resolver**: binds the requester to an authenticated workload identity.
- **Policy decision point (PDP)**: evaluates the normalized action and authority.
- **Policy enforcement point (PEP)**: prevents invocation unless authorized.
- **Approval authority**: issues a bounded, expiring, single-use approval.
- **Executor**: performs the side effect.
- **Receipt signer**: signs the canonical receipt.
- **Verifier**: independently validates proof without access to the enforcement service.

Roles MAY be implemented by separate services. A production deployment SHOULD separate verification from enforcement.

## 3. Processing sequence

1. The PEP MUST receive an envelope conforming to the governed-action schema.
2. It MUST resolve the authenticated workload identity and MUST reject a mismatch with `agent_identity`.
3. It MUST normalize the action before policy evaluation.
4. The PDP MUST evaluate capability, scope, environment, risk, delegation, payload hash, and approval state.
5. When approval is required, the PEP MUST validate and atomically consume a bounded approval before invocation.
6. The PEP MUST persist pre-execution evidence before invoking the executor.
7. It MUST NOT invoke the executor for `DENY` or `HOLD` decisions.
8. For `ALLOW`, it MAY invoke the executor once using the envelope's idempotency key.
9. It MUST bind the attempted/not-attempted state and result to a receipt.
10. The signer MUST sign the canonical receipt bytes excluding `signature`.
11. The verifier MUST be able to reproduce the verification result using the receipt, schema, canonicalization rules, and public key material.

## 4. Decisions and execution states

Allowed policy decisions are:

- `ALLOW`: invocation is permitted.
- `HOLD`: invocation is not permitted until a separate approval is presented.
- `DENY`: invocation is prohibited under the evaluated authority and policy.

Allowed execution states are:

- `NOT_ATTEMPTED`
- `SUCCEEDED`
- `FAILED`
- `UNKNOWN`

`HOLD` and `DENY` MUST have execution state `NOT_ATTEMPTED`. A verifier MUST reject contradictory combinations.

## 5. Canonicalization and hashing

Objects MUST be serialized using the JSON Canonicalization Scheme (RFC 8785) before hashing or signing. Hash identifiers use the multiform `algorithm:lowercase-hex`, initially `sha256:<64 hex characters>`.

`record_hash` is SHA-256 over the canonical receipt with both `record_hash` and `signature` omitted.

`previous_record_hash` is absent for the first record in a chain. Otherwise it MUST equal the immediately preceding record's `record_hash`.

The signature input is the canonical receipt with `signature` omitted and with `record_hash` present.

## 6. Authority and approvals

An authority claim MUST bind:

- subject identity;
- capability;
- resource scope;
- tenant and environment;
- validity interval;
- issuer;
- delegation depth or chain.

Approval MUST be narrower than or equal to the requested envelope. Approval references MUST be unguessable. Single-use approval MUST be consumed atomically before invocation. Failed executor calls MUST NOT make an approval reusable.

## 7. Idempotency

The PEP MUST bind the idempotency key to the normalized action and payload hash. Reuse with a different action or payload MUST be denied. Concurrent duplicate requests MUST result in at most one executor invocation.

## 8. Key resolution and rotation

Receipts identify the signature algorithm and key ID. Verifiers MUST resolve keys from a trusted key set and MUST reject unknown or revoked keys. Historical receipts remain verifiable when the signing key was valid at `issued_at`, subject to the verifier's trust policy.

## 9. Privacy

Receipts SHOULD contain hashes or stable references rather than secrets or raw sensitive payloads. Receipt publication does not imply that action payloads are safe to disclose.

## 10. Conformance

A conforming PEP passes the attack cases in `THREAT_MODEL.md` and never invokes an executor after `HOLD` or `DENY`. A conforming verifier implements every mandatory check in `VERIFICATION_CONTRACT.md` and returns machine-readable findings.

## 11. Adapters

Adapters for Python callables, MCP tools, REST APIs, LangChain tools, and NVIDIA NOOA capabilities MUST preserve the same envelope, decision, pre-invocation boundary, and receipt semantics. Framework-specific metadata MAY be carried in extension fields but MUST NOT weaken core checks.

