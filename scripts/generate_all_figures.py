"""Generate all ten manuscript figures from frozen accepted analytical outputs."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    """Import the installed/local package and generate all figures."""

    from battery_degradation_publication.rendering import generate_figures

    return generate_figures()


if __name__ == "__main__":
    raise SystemExit(main())
