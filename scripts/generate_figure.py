"""Generate one manuscript figure from frozen accepted analytical outputs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    """Parse the requested identifier and render exactly one figure."""

    from battery_degradation_publication.rendering import generate_figures

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--figure", required=True)
    arguments = parser.parse_args()
    return generate_figures([arguments.figure])


if __name__ == "__main__":
    raise SystemExit(main())
