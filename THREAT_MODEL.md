# Threat Model

## Protected properties

- Unauthorized actions do not reach the side-effecting executor.
- An approval cannot authorize a broader identity, capability, scope, payload, tenant, or environment.
- One approval cannot be replayed.
- Duplicate delivery causes at most one side effect.
- Receipts reveal tampering, broken chain continuity, unknown signing keys, and contradictory execution claims.

## Trust boundaries

The requester and action payload are untrusted. Framework adapters are enforcement-critical. Identity, policy, approval storage, key management, durable evidence storage, and executor transports are distinct trust boundaries. The verifier trusts only its configured schemas, canonicalization implementation, trust roots, revocation policy, and local clock.

## Required attack cases

| Attack | Required outcome |
|---|---|
| Bypass adapter and call executor | Executor rejects absent/invalid execution authorization, or network boundary blocks access |
| Undelegated capability | `DENY`, not attempted |
| Scope amplification | `DENY`, not attempted |
| Expired authority | `DENY`, not attempted |
| Approval replay | first bounded use only; later use `DENY` |
| Duplicate execution | same binding returns prior outcome; executor invoked at most once |
| Wrong/unknown signing key | verifier failure |
| Malformed receipt | verifier failure |
| Missing evidence | verifier failure or explicit incomplete status under declared profile |
| Policy timeout/error | fail closed; not attempted |
| Mixed-version records | validate each supported version; reject unsupported downgrade |
| Key rotation | correct historical key verifies; revoked/unknown key fails per trust policy |
| Receipt tampering | record-hash and/or signature failure |
| Identity-envelope mismatch | `DENY`, not attempted |

## Non-goals

OAECP does not prove that:

- a model or agent is inherently safe;
- policy is wise or complete;
- an authorized action has no harmful consequences;
- an executor truthfully reported every external effect;
- a compromised host preserved secrets;
- logs alone prevented bypass.

End-to-end deployments must place the executor behind a boundary that only accepts PEP-authorized calls. A decorator alone is not a sufficient security perimeter when callers can reach the underlying tool directly.

