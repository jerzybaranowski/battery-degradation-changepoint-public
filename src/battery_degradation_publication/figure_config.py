"""Resolve release-local figure configuration and output paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PACKAGE_ROOT / "configs/figure-config.yaml"


@dataclass(frozen=True)
class FigureSpec:
    """Resolved immutable settings for one manuscript figure.

    Parameters
    ----------
    figure_id:
        Stable manuscript filename stem.
    width_in, height_in:
        Physical output dimensions in inches.
    panel_count:
        Expected number of Matplotlib axes.
    style:
        Package-relative Matplotlib style filename.
    """

    figure_id: str
    width_in: float
    height_in: float
    panel_count: int
    style: str


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    """Load the release figure configuration.

    Raises
    ------
    FileNotFoundError
        If the YAML file does not exist.
    ValueError
        If the top-level ``figures`` mapping is absent.
    """

    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or not isinstance(config.get("figures"), dict):
        raise ValueError(f"Invalid figure configuration: {path}")
    return config


def resolve_figure(figure_id: str, config: dict[str, Any] | None = None) -> FigureSpec:
    """Resolve one known figure identifier or raise a clear error."""

    resolved = config or load_config()
    if figure_id not in resolved["figures"]:
        known = ", ".join(resolved["figures"])
        raise ValueError(f"Unknown figure identifier {figure_id!r}. Known figures: {known}")
    entry = resolved["figures"][figure_id]
    return FigureSpec(
        figure_id=figure_id,
        width_in=float(entry["width_in"]),
        height_in=float(entry["height_in"]),
        panel_count=int(entry["panel_count"]),
        style=str(entry["style"]),
    )
