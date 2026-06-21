"""Registry of the ten deterministic manuscript-figure builders."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from matplotlib.figure import Figure

from ._builders import FigureBuildConfig
from .battery11_truncation import build_figure as build_battery11_truncation
from .cd_trajectories import build_figure as build_cd_trajectories
from .h5_ppc import build_figure as build_h5_ppc
from .h5_selected_fits import build_figure as build_h5_selected_fits
from .h5_slope_acceleration import build_figure as build_h5_slope_acceleration
from .h5_transition_midpoints import build_figure as build_h5_transition_midpoints
from .post_transition_horizon import build_figure as build_post_transition_horizon
from .random_thinning import build_figure as build_random_thinning
from .transition_definitions import build_figure as build_transition_definitions
from .truncation_sensitivity import build_figure as build_truncation_sensitivity

Builder = Callable[[Mapping[str, Any], FigureBuildConfig], Figure]

FIGURE_BUILDERS: dict[str, Builder] = {
    "fig_results_cd_trajectories": build_cd_trajectories,
    "fig_results_transition_definitions": build_transition_definitions,
    "fig_results_h5_transition_midpoints": build_h5_transition_midpoints,
    "fig_results_h5_slope_acceleration": build_h5_slope_acceleration,
    "fig_results_h5_selected_fits": build_h5_selected_fits,
    "fig_results_h5_ppc": build_h5_ppc,
    "fig_results_random_thinning": build_random_thinning,
    "fig_results_truncation_sensitivity": build_truncation_sensitivity,
    "fig_results_post_transition_horizon": build_post_transition_horizon,
    "fig_results_battery11_truncation": build_battery11_truncation,
}

__all__ = ["FIGURE_BUILDERS", "FigureBuildConfig"]
