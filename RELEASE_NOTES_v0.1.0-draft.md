# OAECP v0.1.0-draft — Public Reference Implementation

OAECP v0.1.0-draft is an open, model-neutral profile and reference implementation for governing consequential AI-agent actions at the point of use and producing independently verifiable execution receipts.

## Release identity

- Tag: `v0.1.0-draft`
- Commit: `577b391d98fb9d2d90b150617818cacd90507f9a`
- License: Apache-2.0
- Repository: https://github.com/Strixgov/open-agent-execution-control

## Included

- Normative OAECP draft
- Governed-action and signed-receipt JSON Schemas
- Threat model and verification contract
- Python point-of-use enforcement reference
- Offline Ed25519 verifier
- Public JWKS and PEM verification keys
- Four-action signed proof bundle
- Conformance tests
- Alliance, OpenSSF, and Akrites contribution materials

## Demonstrated outcomes

- Repository inspection: `ALLOW`, executor invoked
- Patch proposal: `ALLOW`, executor invoked
- Production merge: `HOLD`, executor not invoked
- Credential rotation: `DENY`, executor not invoked

Each outcome produces a signed receipt. The complete four-record chain can be verified offline without a Strix account.

## Reproduce

```bash
git clone https://github.com/Strixgov/open-agent-execution-control.git
cd open-agent-execution-control
git checkout v0.1.0-draft
python -m pip install --requirement requirements.txt
python run_conformance.py
```

Verify the published bundle:

```bash
python -m reference.verify_all
```

## Important limitations

This is a draft contribution and tested reference implementation. It is not:

- an adopted standard;
- an external certification;
- a complete production integration;
- a fully hardened authorization service;
- a claim of full RFC 8785 implementation conformance.

See `docs/OAECP_PUBLIC_REVIEW_AND_USAGE_GUIDE.md` for the complete limitations and roadmap.
