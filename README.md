# Open Agent Execution Control Profile

An open, model-neutral reference for governing consequential agent actions at the point of use and producing independently verifiable execution receipts.

This clean-room draft is a proposed Strix Gov contribution to the Open Secure AI Alliance and the broader open-source security community. It is not an official Alliance specification, external certification, or production-ready authorization system.

- Public organization: <https://github.com/Strixgov>
- Public repository: <https://github.com/Strixgov/open-agent-execution-control>
- Pinned draft tag: `v0.1.0-draft`
- Pinned draft commit: `577b391d98fb9d2d90b150617818cacd90507f9a`
- License: Apache-2.0

## What is included

- `OPEN_AGENT_EXECUTION_CONTROL_PROFILE.md` — normative protocol draft
- `schemas/governed-action-envelope.schema.json` — action request contract
- `schemas/signed-execution-receipt.schema.json` — receipt contract
- `THREAT_MODEL.md` — threats, trust boundaries, and non-goals
- `VERIFICATION_CONTRACT.md` — independent verification algorithm
- `ALLIANCE_BRIEF.md` — one-page positioning brief
- `OUTREACH.md` — submission-ready outreach copy and missing-input checklist
- `docs/OAECP_PUBLIC_REVIEW_AND_USAGE_GUIDE.md` — public review, usage guide, limitations, and roadmap
- `LICENSE` — Apache License 2.0
- `reference/` — dependency-light Python reference implementation
- `tests/` — conformance tests

## Quick start

Requires Python 3.11+.

```bash
git clone https://github.com/Strixgov/open-agent-execution-control.git
cd open-agent-execution-control
git checkout v0.1.0-draft
python -m pip install --requirement requirements.txt
python run_conformance.py
```

The demo creates a fresh `proof-bundle/` containing four outcomes:

1. repository inspection: allowed and executed;
2. patch proposal: allowed and executed;
3. production merge: held before invocation;
4. credential rotation: denied before invocation.

The one-command run executes the conformance suite, regenerates the four signed receipts and pinned JWKS, and independently verifies the complete hash chain.

Expected high-level result:

```text
Ran 16 tests
OK
executor_calls: ["inspect", "patch"]
all four receipts: valid
aggregate verification: valid
```

Verify the published bundle separately:

```bash
python -m reference.verify_all
```

## Demonstrated trust claim

The published demonstration shows a tested subset of OAECP:

- `ALLOW` can reach the executor;
- `HOLD` and `DENY` do not reach the executor;
- each outcome produces a signed receipt;
- the four-record proof bundle can be verified offline.

It does not establish full RFC 8785 conformance, production durability, external certification, framework-adapter coverage, or Alliance adoption.

## Security status

This is a reference implementation, not a production authorization system. It demonstrates deterministic demo canonicalization, policy decisions, single-use approval consumption, pre-invocation enforcement, Ed25519 signing, hash chaining, and independent verification.

Production deployments still need hardened key management, durable transaction semantics, authenticated identity resolution, policy distribution, audit retention, crash recovery, concurrency controls, tenant isolation, and a protected executor boundary.

See `docs/OAECP_PUBLIC_REVIEW_AND_USAGE_GUIDE.md` for the complete review, limitations, roadmap, diagrams, and FAQ.
