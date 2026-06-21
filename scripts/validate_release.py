"""Validate release checksums, contents, and generated figure artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Validation must not create the cache directories that it is responsible for
# detecting in a clean publication package.
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    """Run package validation and return a shell-compatible status."""

    from battery_degradation_publication.validation import validate_release

    report = validate_release(ROOT)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
