# Open Agent Execution Control Profile

An open, model-neutral reference for governing consequential agent actions at the point of use and producing independently verifiable execution receipts.

This clean-room draft is a proposed Strix Gov contribution to the Open Secure AI Alliance and the broader open-source security community. It is not an official Alliance specification.

Strix Gov public GitHub organization: <https://github.com/Strixgov>

## What is included

- `OPEN_AGENT_EXECUTION_CONTROL_PROFILE.md` — normative protocol draft
- `schemas/governed-action-envelope.schema.json` — action request contract
- `schemas/signed-execution-receipt.schema.json` — receipt contract
- `THREAT_MODEL.md` — threats, trust boundaries, and non-goals
- `VERIFICATION_CONTRACT.md` — independent verification algorithm
- `ALLIANCE_BRIEF.md` — one-page positioning brief
- `OUTREACH.md` — submission-ready outreach copy and missing-input checklist
- `LICENSE` — Apache License 2.0
- `reference/` — dependency-light Python reference implementation
- `tests/` — conformance tests

## Quick start

Requires Python 3.11+ and the `cryptography` package.

```bash
python -m pip install cryptography
python run_conformance.py
```

The demo creates a fresh `proof-bundle/` containing four outcomes:

1. repository inspection: allowed and executed;
2. patch proposal: allowed and executed;
3. production merge: held before invocation;
4. credential rotation: denied before invocation.

The one-command run executes the conformance suite, regenerates the four signed
receipts and pinned JWKS, and independently verifies the complete hash chain.

## Security status

This is a reference implementation, not a production authorization system. It demonstrates canonicalization, policy decisions, single-use approval consumption, pre-invocation enforcement, Ed25519 signing, hash chaining, and independent verification. Production deployments still need hardened key management, durable transaction semantics, authenticated identity resolution, policy distribution, audit retention, and operational review.
