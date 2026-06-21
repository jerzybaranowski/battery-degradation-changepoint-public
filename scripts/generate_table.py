"""Generate one active manuscript table."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    """Parse one table identifier and generate its CSV and LaTeX outputs."""

    from battery_degradation_publication.tables import generate_tables

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", required=True)
    arguments = parser.parse_args()
    return generate_tables([arguments.table])


if __name__ == "__main__":
    raise SystemExit(main())
