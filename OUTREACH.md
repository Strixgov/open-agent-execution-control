# Outreach Package

Public contribution: <https://github.com/Strixgov/open-agent-execution-control>

Pinned draft:

- Tag: `v0.1.0-draft`
- Commit: `577b391d98fb9d2d90b150617818cacd90507f9a`
- License: Apache-2.0

## NVIDIA Alliance form

Verified form fields as of 2026-07-27:

- First Name
- Last Name
- Business Email Address
- Organization / University Name
- Industry
- Job Title
- Location
- Preferred Language
- GitHub Profile or Organization URL
- Company Size
- "How can we help?" choice
- optional question
- privacy-processing consent
- international-transfer consent

**GitHub Profile or Organization URL:** https://github.com/Strixgov

### Proposed response

Strix Gov builds an execution-control kernel for AI agents and automated systems. Strix sits between agent intent and real-world side effects, evaluates authority and policy at point of use, blocks unauthorized actions before execution, and produces canonical signed receipts that can be independently verified without access to Strix.

We have published OAECP v0.1.0-draft, an open Agent Execution Control Profile and tested reference implementation:

https://github.com/Strixgov/open-agent-execution-control

The contribution includes a model- and harness-neutral governed-action envelope; a canonical signed execution-receipt format; an offline verifier; public JWKS and PEM key material; conformance tests; and a reproducible secure-coding demonstration showing authorized actions executing while approval-dependent and undelegated side effects are stopped before invocation.

The published demonstration allows repository inspection and patch proposal, holds production merge for approval, denies undelegated credential rotation, and produces an Ed25519-signed receipt for every outcome. The four-record result can be reproduced offline without a Strix account.

This complements identity, isolation, scanning, and secure model formats by addressing the final runtime question: once an agent has access, what is it authorized to do, and can that enforcement be independently proven?

OAECP is a draft contribution, not an adopted standard, external certification, or complete production integration. We are prepared to contribute engineering resources, specifications, tests, framework adapters, and implementation hardening under Apache-2.0.

### Inputs still required before submission

- applicant first and last name;
- business email;
- industry selection;
- job title selection;
- location;
- preferred language;
- company size;
- affirmative privacy and international-transfer consents.

## OpenSSF introduction

**Subject:** Published draft: point-of-action agent authorization and signed execution receipts

Strix Gov has published OAECP v0.1.0-draft, an open, vendor-neutral Agent Execution Control Profile for consequential AI-agent tool calls:

https://github.com/Strixgov/open-agent-execution-control

The draft standardizes a governed-action envelope, point-of-use authority evaluation, pre-invocation enforcement, bounded single-use approvals, canonical signed execution receipts, offline verification, and conformance tests for replay, scope amplification, bypass, duplicate execution, and malformed evidence.

The public package includes the normative draft, schemas, threat model, Python reference implementation, verifier, JWKS and PEM key material, four signed proof receipts, and reproducible tests under Apache-2.0.

We believe this can complement OpenSSF's AI/ML Security and Supply Chain Integrity work, particularly where automated security agents propose patches, merge changes, disclose vulnerabilities, or affect deployment systems. We would value technical review and guidance on the best working-group venue.

OAECP remains a public draft and tested reference implementation; it is not an adopted standard or production-ready authorization system.

## Akrites introduction

**Subject:** Published engineering contribution: governed agent remediation actions

Strix Gov has published an initial open contribution addressing safe execution of AI-assisted vulnerability-remediation actions:

https://github.com/Strixgov/open-agent-execution-control

OAECP governs whether an identified agent may inspect, patch, merge, disclose, deploy, or rotate credentials at the moment of action. It stops held or undelegated side effects before invocation and binds each decision and execution outcome to an independently verifiable signed receipt.

The public draft includes specifications, schemas, conformance tests, a Python reference implementation, offline verifier, and reproducible secure-coding demonstration under Apache-2.0.

This is intended to complement coordinated remediation and disclosure processes with a portable enforcement and proof layer. We would welcome technical review and discussion of a concrete adapter or conformance profile.
