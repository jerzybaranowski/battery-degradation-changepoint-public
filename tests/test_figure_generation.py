"""Tests for deterministic figure construction and generated outputs."""

import matplotlib.pyplot as plt
import pytest
from battery_degradation_publication.data import load_figure_data
from battery_degradation_publication.figure_config import load_config, resolve_figure
from battery_degradation_publication.figures import FIGURE_BUILDERS, FigureBuildConfig


@pytest.mark.parametrize("figure_id", list(FIGURE_BUILDERS))
def test_builders_return_expected_panel_count(figure_id: str) -> None:
    """Each builder must preserve configured dimensions and panel structure."""

    config = load_config()
    spec = resolve_figure(figure_id, config)
    figure = FIGURE_BUILDERS[figure_id](
        load_figure_data(),
        FigureBuildConfig(width_in=spec.width_in, height_in=spec.height_in),
    )
    try:
        assert len(figure.axes) == spec.panel_count
        assert tuple(figure.get_size_inches()) == pytest.approx((spec.width_in, spec.height_in))
    finally:
        plt.close(figure)
