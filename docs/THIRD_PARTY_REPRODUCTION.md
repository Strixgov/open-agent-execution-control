# Third-Party Reproduction Request

Strix Gov is requesting an independent reproduction of OAECP `v0.1.0-draft`.

## Repository and pin

- Repository: https://github.com/Strixgov/open-agent-execution-control
- Tag: `v0.1.0-draft`
- Commit: `577b391d98fb9d2d90b150617818cacd90507f9a`

## Commands

```bash
git clone https://github.com/Strixgov/open-agent-execution-control.git
cd open-agent-execution-control
git checkout v0.1.0-draft
python -m pip install --requirement requirements.txt
python run_conformance.py
python -m reference.verify_all
```

## Please report

- Name or organization, if attribution is permitted
- Operating system
- Python version
- Checked-out commit SHA
- Dependency versions
- Complete test output
- Complete verification output
- Whether only `inspect` and `patch` reached the executor
- Whether all four receipts verified
- Any discrepancies, warnings, or ambiguous claims

## Expected high-level result

```text
Ran 16 tests
OK
executor_calls: ["inspect", "patch"]
all four receipts: valid
aggregate verification: valid
```

## Claim boundary

A successful reproduction confirms that the published reference package behaves as documented in the reproducer's environment. It does not certify production readiness, Alliance adoption, legal compliance, or the absence of ungoverned execution paths in other systems.
