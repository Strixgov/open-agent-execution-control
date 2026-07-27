# Outreach Package

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

We would like to contribute an open Agent Execution Control Profile to the Open Secure AI Alliance. The contribution includes a model- and harness-neutral governed-action envelope; a canonical signed execution-receipt format; an independent verifier; conformance tests for bypass, replay, scope amplification, expired authority, malformed evidence, duplicate execution, and key rotation; reference adapters for NVIDIA NOOA, LangChain, Python, MCP-style tools, and REST actions; and a reproducible secure-coding demonstration showing authorized actions executing and unauthorized side effects being blocked before invocation.

This complements identity, isolation, scanning, and secure model formats by addressing the final runtime question: once an agent has access, what is it authorized to do, and can that enforcement be independently proven?

We are prepared to contribute engineering resources, specifications, tests, and a live reference implementation under an open license.

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

Subject: Proposed open profile for point-of-action agent authorization and signed execution receipts

Strix Gov is preparing an open, vendor-neutral Agent Execution Control Profile for consequential AI-agent tool calls. The draft standardizes a governed-action envelope, point-of-use authority evaluation, pre-invocation enforcement, bounded single-use approvals, canonical signed execution receipts, offline verification, and conformance tests for replay, scope amplification, bypass, key rotation, and malformed evidence.

We believe this can complement OpenSSF's AI/ML Security and Supply Chain Integrity work, particularly where automated security agents propose patches, merge changes, disclose vulnerabilities, or affect deployment systems. We would value technical review and guidance on the best working-group venue. The draft, schemas, verifier, and reproducible demo will be released under Apache-2.0.

## Akrites introduction

Subject: Engineering contribution proposal: governed agent remediation actions

Strix Gov would like to contribute engineering work around safe execution of AI-assisted vulnerability-remediation actions. Our proposed open profile governs whether an identified agent may inspect, patch, merge, disclose, deploy, or rotate credentials at the moment of action, blocks undelegated side effects before invocation, and binds the decision and execution result to an independently verifiable signed receipt.

This is intended to complement Akrites' coordinated remediation and disclosure process with a portable enforcement and proof layer. We can contribute specifications, schemas, conformance tests, adapters, and a live secure-coding demonstration under an open license.
