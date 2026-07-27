# Independent Verification Contract

Input: one receipt, the matching schemas, trusted public keys, optional predecessor receipt, key validity/revocation data, and verifier time.

The verifier MUST:

1. parse JSON with duplicate-key rejection;
2. reject unsupported profile versions;
3. validate the receipt and embedded envelope against their schemas;
4. recompute `record_hash` from canonical receipt content with `record_hash` and `signature` omitted;
5. compare computed and stored hashes in constant time;
6. resolve `signature.key_id` from the configured trust set;
7. confirm the key and algorithm were valid at `issued_at`;
8. verify the Ed25519 signature over canonical receipt content excluding `signature`;
9. if a predecessor is supplied, recompute its hash and compare it with `previous_record_hash`;
10. verify authority subject equals request agent identity;
11. verify capability binding is consistent with the decision: `ALLOW` and `HOLD`
    require the capability to be present; `DENY` may prove that it is absent;
12. require policy status `EVALUATED`;
13. enforce decision/execution consistency:
    - `ALLOW` permits attempted execution;
    - `HOLD` and `DENY` require `authorized=false`, `attempted=false`, and `NOT_ATTEMPTED`;
14. require an execution result hash for `SUCCEEDED`;
15. return separate findings for structure, record hash, signature, chain, authority binding, policy, and execution consistency.

The verifier MUST NOT report an overall success if any mandatory finding fails. It SHOULD provide JSON output suitable for automation and MUST NOT require a Strix account or network call.

The reference code uses a deterministic JSON encoding compatible with the data types emitted by the demo. Production implementations MUST use a complete RFC 8785 implementation.
