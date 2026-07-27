from __future__ import annotations

import json
from pathlib import Path

from .verify import load_jwks, verify


def main() -> None:
    bundle = Path("proof-bundle")
    trust = load_jwks((bundle / "jwks.json").read_bytes())
    paths = [
        bundle / "receipt-inspect-allowed.json",
        bundle / "receipt-patch-allowed.json",
        bundle / "receipt-merge-held.json",
        bundle / "receipt-credential-rotation-denied.json",
    ]
    predecessor = None
    results = []
    for path in paths:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        result = verify(receipt, trust, predecessor)
        results.append({"receipt": path.name, **result})
        predecessor = receipt
    output = {"valid": all(item["valid"] for item in results), "results": results}
    print(json.dumps(output, indent=2))
    raise SystemExit(0 if output["valid"] else 1)


if __name__ == "__main__":
    main()

