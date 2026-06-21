"""Render configured figures with release-local styles and deterministic paths."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from .data import load_figure_data
from .figure_config import PACKAGE_ROOT, load_config, resolve_figure
from .figures import FIGURE_BUILDERS, FigureBuildConfig


def generate_figures(figure_ids: Sequence[str] | None = None) -> int:
    """Render selected figures as PDF and 300-DPI PNG files.

    Parameters
    ----------
    figure_ids:
        Stable figure identifiers. ``None`` renders all configured figures.

    Returns
    -------
    int
        Zero after successful generation.
    """

    config = load_config()
    selected = list(figure_ids) if figure_ids is not None else list(config["figures"])
    unknown = [figure_id for figure_id in selected if figure_id not in FIGURE_BUILDERS]
    if unknown:
        known = ", ".join(FIGURE_BUILDERS)
        raise ValueError(f"Unknown figure identifier(s): {unknown}. Known figures: {known}")
    output_directory = PACKAGE_ROOT / "figures/generated"
    output_directory.mkdir(parents=True, exist_ok=True)
    data = load_figure_data()
    for figure_id in selected:
        spec = resolve_figure(figure_id, config)
        style_path = PACKAGE_ROOT / "configs" / spec.style
        if not style_path.is_file():
            raise FileNotFoundError(f"Figure style is missing: {style_path}")
        with plt.style.context(style_path):
            figure = FIGURE_BUILDERS[figure_id](
                data,
                FigureBuildConfig(width_in=spec.width_in, height_in=spec.height_in),
            )
            if len(figure.axes) != spec.panel_count:
                plt.close(figure)
                raise ValueError(
                    f"{figure_id} produced {len(figure.axes)} axes; expected {spec.panel_count}"
                )
            try:
                figure.savefig(
                    output_directory / f"{figure_id}.pdf",
                    metadata={"Creator": "battery-degradation-publication"},
                )
                figure.savefig(
                    output_directory / f"{figure_id}.png",
                    dpi=int(config["rendering"]["png_dpi"]),
                )
            except OSError as exc:
                raise OSError(f"Could not write outputs for {figure_id}: {exc}") from exc
            finally:
                plt.close(figure)
    return 0
