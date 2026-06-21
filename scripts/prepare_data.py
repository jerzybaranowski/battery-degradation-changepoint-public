"""Validate an optional local copy of the public raw dataset.

Figure generation does not require this file because the release distributes the
accepted frozen plotting tables. This command supports an independent provenance
check when the user has legally obtained the source CSV.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    """Validate a locally acquired raw CSV and print its audit summary."""

    from battery_degradation_publication.raw_data import validate_raw_dataset

    try:
        report = validate_raw_dataset(ROOT / "data/raw/data_new.csv")
    except (FileNotFoundError, ValueError) as exc:
        print(f"Raw-data validation failed: {exc}", file=sys.stderr)
        return 2
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
