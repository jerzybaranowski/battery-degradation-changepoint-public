"""Generate all active manuscript tables without statistical re-estimation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    """Import the installed/local package and generate all active tables."""

    from battery_degradation_publication.tables import generate_tables

    return generate_tables()


if __name__ == "__main__":
    raise SystemExit(main())
