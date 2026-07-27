# Strix Gov: Runtime Authority and Proof for Open Agent Defense

The Open Secure AI Alliance is assembling an open defense stack spanning identity, model formats, isolation, scanning, secure coding, harnesses, permissions, and evaluation. Strix Gov proposes a complementary missing layer: point-of-action authority evaluation, pre-invocation enforcement, and independently verifiable proof.

## Proposed open contribution

The **Open Agent Execution Control Profile** defines:

- a model- and harness-neutral governed action envelope;
- a canonical signed execution receipt;
- a verifier that needs no Strix service or account;
- conformance tests for bypass, replay, scope amplification, expired authority, malformed evidence, duplicate execution, and key rotation;
- reference adapters for ordinary Python, MCP-style tools, REST APIs, LangChain, and NVIDIA NOOA;
- a reproducible secure-coding demonstration.

## Demonstration

A defensive agent can inspect a repository and propose a patch. It cannot merge to production without approval or rotate credentials outside its delegation. Every allow, hold, denial, and execution outcome is represented by a signed receipt that a third party can verify offline.

## Architectural fit

Identity establishes who the agent is. Isolation limits where it can run. Strix determines what the identified agent is authorized to do at the moment of action and produces evidence that independent parties can verify.

The contribution is deliberately narrow. It is not a model safeguard, vulnerability scanner, observability product, sandbox, or claim that an agent is inherently safe.

## Contribution commitment

Strix Gov is prepared to contribute specifications, schemas, tests, reference adapters, demonstration code, and engineering time under an open license.

