"""Publication-profile result figures built from accepted analytical artifacts.

The module is deliberately restricted to data loading, schema validation, and Matplotlib
construction. It does not fit models, sample posteriors, recompute uncertainty intervals, or
modify analytical artifacts. Every plotted numerical summary is loaded from an existing
repository output produced by the authoritative analysis pipeline.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

PACKAGE_ROOT = Path(__file__).resolve().parents[3]
FROZEN_ROOT = PACKAGE_ROOT / "data/frozen_results"
M4_RUN = FROZEN_ROOT / "m4"
M4_COMPARISON = FROZEN_ROOT / "m4"
H5_RUN = FROZEN_ROOT / "h5"
PPC_ROOT = FROZEN_ROOT / "ppc"
M8_ROOT = FROZEN_ROOT / "m8"
M8_ASSETS = FROZEN_ROOT / "m8"

BLUE = {
    "light": "#B3FFFF",
    "light_highlight": "#9AF6FF",
    "mid": "#67C3FF",
    "mid_highlight": "#3490CC",
    "dark": "#015D99",
    "dark_highlight": "#002A66",
}
YELLOW = {"light": "#FFFFAA", "dark": "#EECA02", "dark_highlight": "#D5B100"}
NEUTRAL = {
    "light": "#D9D9D9",
    "mid": "#8C8C8C",
    "dark": "#4D4D4D",
    "near_black": "#1A1A1A",
}


@dataclass(frozen=True)
class FigureBuildConfig:
    """Resolved rendering inputs for one publication figure.

    Parameters
    ----------
    width_in, height_in:
        Physical dimensions in inches.
    """

    width_in: float
    height_in: float


def _read_csv(path: Path, required: set[str]) -> pd.DataFrame:
    """Read an authoritative CSV and require all declared columns.

    Parameters
    ----------
    path:
        Existing analytical artifact.
    required:
        Columns required by a figure builder.

    Returns
    -------
    pandas.DataFrame
        Unmodified table in artifact row order.

    Raises
    ------
    FileNotFoundError
        If the analytical artifact is absent.
    ValueError
        If required columns are missing.
    """

    if not path.exists():
        raise FileNotFoundError(path)
    frame = pd.read_csv(path)
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"{path} is missing required columns: {missing}")
    return frame


def load_publication_figure_data() -> dict[str, Any]:
    """Load and validate all prepared artifacts required by Figures R1--R10.

    Returns
    -------
    dict
        Tables and JSON summaries keyed by stable analytical role. No filtering, aggregation,
        uncertainty calculation, smoothing, interpolation, or model computation is performed.
    """

    import json

    data: dict[str, Any] = {
        "regular_rows": _read_csv(
            H5_RUN / "regular_eligible_cycles.csv",
            {"Battery_ID", "Cycle_Index", "C/D"},
        ),
        "aggregate_complete": _read_csv(
            M4_RUN / "regular_eligible_cycle_aggregate_complete.csv",
            {
                "cycle_index",
                "n_batteries",
                "value_median",
                "value_lower_quantile",
                "value_upper_quantile",
            },
        ),
        "aggregate_retained": _read_csv(
            M4_RUN / "regular_eligible_cycle_aggregate.csv",
            {"cycle_index", "n_batteries", "value"},
        ),
        "m4_summary": _read_csv(
            M4_COMPARISON / "changepoint_method_summary.csv",
            {
                "method",
                "changepoint_cycle",
                "interval_lower",
                "interval_upper",
                "diagnostic_status",
            },
        ),
        "m4_predictions": _read_csv(
            M4_COMPARISON / "changepoint_method_predictions.csv",
            {"method", "cycle_index", "predicted_center"},
        ),
        "m4_curvature": _read_csv(
            M4_COMPARISON / "curvature_sensitivity.csv",
            {"smoothing_parameter", "knee_cycle", "fit_status"},
        ),
        "h5_battery": _read_csv(
            H5_RUN / "accepted_battery_scientific_summary.csv",
            {
                "Battery_ID",
                "tau_median_cycles",
                "tau_hdi_lower_cycles",
                "tau_hdi_upper_cycles",
                "beta_pre_median_cd_per_cycle",
                "beta_pre_hdi_lower_cd_per_cycle",
                "beta_pre_hdi_upper_cd_per_cycle",
                "beta_post_median_cd_per_cycle",
                "beta_post_hdi_lower_cd_per_cycle",
                "beta_post_hdi_upper_cd_per_cycle",
                "delta_beta_median_cd_per_cycle",
                "delta_beta_hdi_lower_cd_per_cycle",
                "delta_beta_hdi_upper_cd_per_cycle",
                "probability_delta_beta_positive",
                "transition_identifiability_flag",
            },
        ),
        "h5_population": _read_csv(
            H5_RUN / "accepted_population_scientific_summary.csv",
            {"quantity", "median", "hdi_lower", "hdi_upper"},
        ),
        "ppc_per_battery": _read_csv(
            PPC_ROOT / "ppc_per_battery_summary.csv",
            {"Battery_ID", "coverage_90", "coverage_95", "boundary_sensitive"},
        ),
        "ppc_binned": _read_csv(
            PPC_ROOT / "ppc_binned_residuals.csv",
            {
                "Battery_ID",
                "cycle_normalized_midpoint",
                "residual_median",
                "absolute_residual_mad",
            },
        ),
        "ppc_trajectory": _read_csv(
            PPC_ROOT / "ppc_trajectory_summary.csv",
            {
                "Battery_ID",
                "cycle_original",
                "observed_response",
                "latent_mean_median",
                "latent_mean_90_lower",
                "latent_mean_90_upper",
                "residual",
            },
        ),
        "random_battery": _read_csv(
            M8_ROOT / "stability_vs_full_data_h1_per_battery.csv",
            {
                "scenario_id",
                "battery_id",
                "tau_shift_cycles",
                "tau_hdi_width_ratio",
            },
        ),
        "random_summary": _read_csv(
            M8_ROOT / "random_thinning_seed_summary.csv",
            {"scope", "scenario_id", "rank_correlation_with_r0"},
        ),
        "a1_stability": _read_csv(
            M8_ROOT / "stability_vs_full_data_a1.csv",
            {"scenario_id", "tau_shift", "tau_hdi_width_change_fraction"},
        ),
        "h1_stability": _read_csv(
            M8_ROOT / "stability_vs_full_data_h1_population.csv",
            {"scenario_id", "tau_shift", "tau_hdi_width_change_fraction"},
        ),
        "truncation": _read_csv(
            M8_ROOT / "truncation_summary.csv",
            {
                "model_id",
                "scenario_id",
                "retained_fraction",
                "tau_shift",
                "tau_hdi_width_ratio",
                "extrapolation_rmse",
                "posterior_predictive_coverage_90",
                "posterior_predictive_coverage_95",
                "tau_rank_correlation_with_r0",
            },
        ),
        "horizon": _read_csv(
            M8_ROOT / "post_transition_horizon_analysis.csv",
            {
                "scenario_id",
                "battery_id",
                "retained_fraction",
                "post_transition_horizon_cycles",
                "absolute_tau_shift_cycles",
                "tau_hdi_width_ratio",
                "availability_class",
                "spearman_tau_shift",
                "spearman_hdi_inflation",
            },
        ),
        "truncation_battery": _read_csv(
            M8_ASSETS / "figure_data_h1_truncation_per_battery.csv",
            {
                "Battery_ID",
                "scenario_id",
                "tau_median",
                "tau_hdi_95_lower",
                "tau_hdi_95_upper",
                "boundary_status",
            },
        ),
        "mask_registry": _read_csv(
            M8_ROOT / "data_mask_registry.csv",
            {"scenario_id", "battery_id", "observed_cycle_max"},
        ),
        "m8_diagnostics": _read_csv(
            M8_ROOT / "computational_diagnostics.csv",
            {"model_id", "scenario_id", "diagnostic_status", "treedepth_saturation_count"},
        ),
    }
    with (PPC_ROOT / "ppc_overall_summary.json").open(encoding="utf-8") as handle:
        data["ppc_overall"] = json.load(handle)

    battery_ids = data["regular_rows"]["Battery_ID"].astype(int).unique().tolist()
    if battery_ids != list(range(1, 15)):
        raise ValueError(f"Expected Battery_ID 1 through 14 in source order, found {battery_ids}")
    return data


def _new_figure(config: FigureBuildConfig, **kwargs: Any) -> Figure:
    """Create a publication figure with exact configured dimensions."""

    return plt.figure(figsize=(config.width_in, config.height_in), layout="constrained", **kwargs)


def _panel_label(axis: Axes, label: str) -> None:
    """Add a compact panel identifier required by the supplied caption drafts."""

    axis.text(
        -0.10,
        1.04,
        label,
        transform=axis.transAxes,
        ha="left",
        va="bottom",
        fontweight="bold",
        color=NEUTRAL["near_black"],
    )


def _clean_axis(axis: Axes) -> None:
    """Apply restrained publication framing without changing the plotted domain."""

    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def build_r1(data: Mapping[str, Any], config: FigureBuildConfig) -> Figure:
    """Build Figure R1: battery trajectories, aggregate spread, and support."""

    rows = data["regular_rows"]
    aggregate = data["aggregate_complete"]
    figure = _new_figure(config)
    grid = figure.add_gridspec(6, 4, height_ratios=[1, 1, 1, 1, 1.25, 0.85])
    small_axes: list[Axes] = []
    for index, battery_id in enumerate(range(1, 15)):
        axis = figure.add_subplot(grid[index // 4, index % 4])
        frame = rows.loc[rows["Battery_ID"].eq(battery_id)]
        axis.plot(frame["Cycle_Index"], frame["C/D"], color=BLUE["dark"], lw=0.55)
        axis.set_title(f"Battery {battery_id}", fontsize=7.5, pad=2)
        axis.tick_params(labelsize=6)
        if index // 4 < 3:
            axis.tick_params(labelbottom=False)
        if index % 4 != 0:
            axis.tick_params(labelleft=False)
        _clean_axis(axis)
        small_axes.append(axis)
    for index in (14, 15):
        axis = figure.add_subplot(grid[index // 4, index % 4])
        axis.axis("off")

    aggregate_axis = figure.add_subplot(grid[4, :])
    supported = aggregate["n_batteries"].ge(7)
    aggregate_axis.fill_between(
        aggregate["cycle_index"],
        aggregate["value_lower_quantile"],
        aggregate["value_upper_quantile"],
        color=BLUE["light_highlight"],
        alpha=0.75,
        label="Interquartile range",
    )
    aggregate_axis.plot(
        aggregate["cycle_index"],
        aggregate["value_median"],
        color=BLUE["dark_highlight"],
        lw=1.2,
        label="Median C/D",
    )
    aggregate_axis.scatter(
        aggregate.loc[~supported, "cycle_index"],
        aggregate.loc[~supported, "value_median"],
        facecolors="none",
        edgecolors=NEUTRAL["mid"],
        s=9,
        linewidths=0.6,
        label="Support < 7",
    )
    aggregate_axis.set_ylabel("C/D")
    aggregate_axis.set_title("Cycle-level aggregate")
    aggregate_axis.legend(ncols=3, loc="upper left")
    _clean_axis(aggregate_axis)

    support_axis = figure.add_subplot(grid[5, :], sharex=aggregate_axis)
    support_axis.step(
        aggregate["cycle_index"],
        aggregate["n_batteries"],
        where="mid",
        color=BLUE["dark"],
        lw=1.0,
    )
    support_axis.axhline(7, color=NEUTRAL["dark"], ls="--", lw=0.9)
    support_axis.text(
        0.99,
        7.25,
        "model threshold = 7",
        transform=support_axis.get_yaxis_transform(),
        ha="right",
        va="bottom",
        fontsize=7,
    )
    support_axis.set_xlabel("Cycle index")
    support_axis.set_ylabel("Batteries")
    support_axis.set_ylim(0, 15)
    _clean_axis(support_axis)
    _panel_label(small_axes[0], "(a)")
    _panel_label(aggregate_axis, "(b)")
    _panel_label(support_axis, "(c)")
    return figure


def build_r2(data: Mapping[str, Any], config: FigureBuildConfig) -> Figure:
    """Build Figure R2: non-equivalent operational transition definitions."""

    observations = data["aggregate_retained"]
    predictions = data["m4_predictions"]
    summary = data["m4_summary"].set_index("method")
    curvature = data["m4_curvature"]
    figure = _new_figure(config)
    grid = figure.add_gridspec(2, 1, height_ratios=[2.2, 1.0])
    top = figure.add_subplot(grid[0])
    bottom = figure.add_subplot(grid[1])

    top.scatter(
        observations["cycle_index"],
        observations["value"],
        s=7,
        color=NEUTRAL["mid"],
        alpha=0.55,
        rasterized=True,
        label="Median aggregate",
    )
    styles = {
        "linear": (NEUTRAL["dark"], ":", "B0 linear"),
        "broken_stick": (BLUE["mid_highlight"], "--", "D1 broken stick"),
        "bayesian_smooth": (BLUE["dark_highlight"], "-", "A1 smooth hinge"),
    }
    for method, (color, line_style, label) in styles.items():
        frame = predictions.loc[predictions["method"].eq(method)]
        top.plot(
            frame["cycle_index"],
            frame["predicted_center"],
            color=color,
            ls=line_style,
            lw=1.35,
            label=label,
        )
    for method, color, y_fraction in [
        ("broken_stick", BLUE["mid_highlight"], 0.06),
        ("bayesian_smooth", BLUE["dark_highlight"], 0.12),
    ]:
        row = summary.loc[method]
        top.axvspan(row["interval_lower"], row["interval_upper"], color=color, alpha=0.10)
        top.axvline(row["changepoint_cycle"], color=color, ls="--", lw=0.9)
        top.text(
            row["changepoint_cycle"],
            y_fraction,
            "D1 breakpoint" if method == "broken_stick" else "A1 midpoint",
            transform=top.get_xaxis_transform(),
            rotation=90,
            ha="right",
            va="bottom",
            color=color,
            fontsize=7,
        )
    top.set_ylabel("Median C/D")
    top.set_title("Aggregate fits and distinct transition estimands")
    top.legend(ncols=2, loc="upper left")
    _clean_axis(top)

    bottom.plot(
        curvature["smoothing_parameter"],
        curvature["knee_cycle"],
        color=BLUE["dark"],
        marker="o",
        lw=1.0,
    )
    bottom.axhspan(
        curvature["knee_cycle"].min(),
        curvature["knee_cycle"].max(),
        color=YELLOW["light"],
        alpha=0.35,
    )
    bottom.text(
        0.99,
        0.94,
        "stability gate failed",
        transform=bottom.transAxes,
        ha="right",
        va="top",
        color=NEUTRAL["dark"],
        fontsize=7,
    )
    bottom.set_xticks(curvature["smoothing_parameter"])
    bottom.set_xlabel("Spline smoothing parameter")
    bottom.set_ylabel("S1 knee cycle")
    bottom.set_title("S1 smoothing sensitivity")
    _clean_axis(bottom)
    _panel_label(top, "(a)")
    _panel_label(bottom, "(b)")
    return figure


def build_r3(data: Mapping[str, Any], config: FigureBuildConfig) -> Figure:
    """Build Figure R3: sorted battery-specific transition midpoint intervals."""

    batteries = data["h5_battery"].sort_values("tau_median_cycles", kind="mergesort")
    population = (
        data["h5_population"].set_index("quantity").loc["population_transition_midpoint_cycles"]
    )
    labels = [f"Battery {int(value)}" for value in batteries["Battery_ID"]]
    y = np.arange(len(batteries))
    figure = _new_figure(config)
    axis = figure.add_subplot(111)
    for position, (_, row) in zip(y, batteries.iterrows(), strict=True):
        battery_id = int(row["Battery_ID"])
        boundary = row["transition_identifiability_flag"] == "boundary_sensitive"
        color = NEUTRAL["dark"] if boundary else BLUE["dark"]
        marker = "D" if boundary else "o"
        face = "white" if boundary else color
        axis.hlines(
            position,
            row["tau_hdi_lower_cycles"],
            row["tau_hdi_upper_cycles"],
            color=color,
            lw=1.3,
        )
        axis.scatter(
            row["tau_median_cycles"],
            position,
            marker=marker,
            facecolors=face,
            edgecolors=color,
            s=30,
            zorder=3,
        )
        if battery_id in {11, 14}:
            text = "earliest" if battery_id == 14 else "boundary-sensitive"
            axis.annotate(
                text,
                (row["tau_median_cycles"], position),
                xytext=(7, 0),
                textcoords="offset points",
                va="center",
                fontsize=7,
                color=color,
            )
    population_y = len(batteries) + 0.8
    axis.hlines(
        population_y,
        population["hdi_lower"],
        population["hdi_upper"],
        color=BLUE["dark_highlight"],
        lw=2.2,
    )
    axis.scatter(
        population["median"],
        population_y,
        marker="*",
        color=BLUE["dark_highlight"],
        s=70,
        zorder=3,
    )
    axis.set_yticks([*y, population_y], [*labels, "Population mean"])
    axis.set_xlabel("Transition midpoint (cycle)")
    axis.set_title("Battery-specific H5.1 transition midpoints")
    axis.invert_yaxis()
    _clean_axis(axis)
    return figure


def build_r4(data: Mapping[str, Any], config: FigureBuildConfig) -> Figure:
    """Build Figure R4: battery-specific pre/post slopes and slope increments."""

    batteries = data["h5_battery"].sort_values("Battery_ID")
    population = data["h5_population"].set_index("quantity")
    labels = [f"Battery {int(value)}" for value in batteries["Battery_ID"]]
    y = np.arange(len(batteries))
    figure = _new_figure(config)
    axes = figure.subplots(1, 2, sharey=True)
    left, right = axes

    for position, (_, row) in zip(y, batteries.iterrows(), strict=True):
        left.plot(
            [row["beta_pre_median_cd_per_cycle"], row["beta_post_median_cd_per_cycle"]],
            [position, position],
            color=NEUTRAL["light"],
            lw=1.2,
        )
        left.scatter(
            row["beta_pre_median_cd_per_cycle"],
            position,
            marker="s",
            facecolors="white",
            edgecolors=BLUE["mid_highlight"],
            s=24,
            label="Pre-transition" if position == 0 else None,
        )
        left.scatter(
            row["beta_post_median_cd_per_cycle"],
            position,
            marker="o",
            color=BLUE["dark"],
            s=24,
            label="Post-transition" if position == 0 else None,
        )
        right.hlines(
            position,
            row["delta_beta_hdi_lower_cd_per_cycle"],
            row["delta_beta_hdi_upper_cd_per_cycle"],
            color=BLUE["dark"],
            lw=1.2,
        )
        right.scatter(row["delta_beta_median_cd_per_cycle"], position, color=BLUE["dark"], s=24)

    pop_pre = population.loc["population_pre_transition_slope_cd_per_cycle"]
    pop_post = population.loc["population_post_transition_slope_cd_per_cycle"]
    pop_delta = population.loc["population_slope_change_cd_per_cycle"]
    pop_y = len(batteries) + 0.8
    left.plot([pop_pre["median"], pop_post["median"]], [pop_y, pop_y], color=NEUTRAL["dark"])
    left.scatter(pop_pre["median"], pop_y, marker="s", facecolors="white", edgecolors=BLUE["dark"])
    left.scatter(pop_post["median"], pop_y, marker="o", color=BLUE["dark_highlight"])
    right.hlines(
        pop_y, pop_delta["hdi_lower"], pop_delta["hdi_upper"], color=BLUE["dark_highlight"], lw=2
    )
    right.scatter(pop_delta["median"], pop_y, marker="*", color=BLUE["dark_highlight"], s=60)
    left.set_yticks([*y, pop_y], [*labels, "Population mean"])
    left.invert_yaxis()
    left.set_xlabel("Slope (C/D per cycle)")
    right.set_xlabel("Slope increment (C/D per cycle)")
    left.set_title("Pre- and post-transition slopes")
    right.set_title("Slope increment with 95% HDI")
    right.axvline(0, color=NEUTRAL["mid"], ls="--", lw=0.8)
    left.legend(loc="lower right")
    _clean_axis(left)
    _clean_axis(right)
    _panel_label(left, "(a)")
    _panel_label(right, "(b)")
    return figure


def build_r5(data: Mapping[str, Any], config: FigureBuildConfig) -> Figure:
    """Build Figure R5: selected accepted H5.1 latent trajectory fits."""

    trajectory = data["ppc_trajectory"]
    batteries = data["h5_battery"].set_index("Battery_ID")
    selected = [14, 1, 3, 11]
    figure = _new_figure(config)
    axes = figure.subplots(2, 2, sharex=True, sharey=True)
    for axis, battery_id in zip(axes.ravel(), selected, strict=True):
        frame = trajectory.loc[trajectory["Battery_ID"].eq(battery_id)]
        summary = batteries.loc[battery_id]
        axis.scatter(
            frame["cycle_original"],
            frame["observed_response"],
            s=4,
            color=NEUTRAL["mid"],
            alpha=0.35,
            rasterized=True,
        )
        axis.fill_between(
            frame["cycle_original"],
            frame["latent_mean_90_lower"],
            frame["latent_mean_90_upper"],
            color=BLUE["light_highlight"],
            alpha=0.75,
        )
        axis.plot(
            frame["cycle_original"],
            frame["latent_mean_median"],
            color=BLUE["dark_highlight"],
            lw=1.2,
        )
        axis.axvspan(
            summary["tau_hdi_lower_cycles"],
            summary["tau_hdi_upper_cycles"],
            color=YELLOW["light"],
            alpha=0.28,
        )
        axis.axvline(summary["tau_median_cycles"], color=NEUTRAL["dark"], ls="--", lw=0.9)
        suffix = " — boundary-sensitive" if battery_id == 11 else ""
        axis.set_title(f"Battery {battery_id}{suffix}")
        _clean_axis(axis)
    figure.supxlabel("Cycle index")
    figure.supylabel("C/D")
    return figure


def build_r6(data: Mapping[str, Any], config: FigureBuildConfig) -> Figure:
    """Build Figure R6: H5.1 posterior predictive calibration and residual structure."""

    overall = data["ppc_overall"]
    per_battery = data["ppc_per_battery"].sort_values("Battery_ID")
    binned = data["ppc_binned"]
    figure = _new_figure(config)
    axes = figure.subplots(2, 2)
    coverage_axis, residual_axis, absolute_axis, battery_axis = axes.ravel()

    nominal = np.array([0.50, 0.80, 0.90, 0.95])
    empirical = np.array(
        [
            overall["coverage_50"],
            overall["coverage_80"],
            overall["coverage_90"],
            overall["coverage_95"],
        ]
    )
    coverage_axis.plot([0.45, 1.0], [0.45, 1.0], color=NEUTRAL["mid"], ls="--", lw=0.9)
    coverage_axis.plot(nominal, empirical, color=BLUE["dark"], marker="o", lw=1.2)
    coverage_axis.set_xlabel("Nominal coverage")
    coverage_axis.set_ylabel("Empirical coverage")
    coverage_axis.set_title("Overall predictive calibration")

    for battery_id, frame in binned.groupby("Battery_ID", sort=True):
        color = NEUTRAL["dark"] if int(battery_id) == 11 else BLUE["mid_highlight"]
        alpha = 0.95 if int(battery_id) == 11 else 0.42
        residual_axis.plot(
            frame["cycle_normalized_midpoint"],
            frame["residual_median"],
            color=color,
            lw=0.85,
            alpha=alpha,
        )
        absolute_axis.plot(
            frame["cycle_normalized_midpoint"],
            frame["absolute_residual_mad"],
            color=color,
            lw=0.85,
            alpha=alpha,
        )
    residual_axis.axhline(0, color=NEUTRAL["mid"], ls="--", lw=0.8)
    residual_axis.set_xlabel("Within-battery normalized cycle")
    residual_axis.set_ylabel("Binned median residual (C/D)")
    residual_axis.set_title("Signed residual structure")
    absolute_axis.set_xlabel("Within-battery normalized cycle")
    absolute_axis.set_ylabel("Binned MAD of residual (C/D)")
    absolute_axis.set_title("Residual magnitude")

    x = np.arange(1, 15)
    colors = [
        NEUTRAL["dark"] if value else BLUE["dark"] for value in per_battery["boundary_sensitive"]
    ]
    battery_axis.scatter(
        x,
        per_battery["coverage_90"],
        color=colors,
        marker="o",
        s=25,
        label="90%",
    )
    battery_axis.scatter(
        x,
        per_battery["coverage_95"],
        facecolors="white",
        edgecolors=colors,
        marker="s",
        s=25,
        label="95%",
    )
    battery_axis.axhline(0.90, color=BLUE["dark"], ls=":", lw=0.8)
    battery_axis.axhline(0.95, color=NEUTRAL["dark"], ls=":", lw=0.8)
    battery_axis.set_xticks(x, [f"B{value}" for value in x], rotation=45)
    battery_axis.set_ylabel("Empirical coverage")
    battery_axis.set_title("Battery-specific calibration")
    battery_axis.legend(ncols=2, loc="lower right")
    for axis, label in zip(axes.ravel(), ["(a)", "(b)", "(c)", "(d)"], strict=True):
        _panel_label(axis, label)
        _clean_axis(axis)
    return figure


def _random_population_rows(data: Mapping[str, Any]) -> pd.DataFrame:
    """Return existing per-mask population shifts and width ratios without recomputation."""

    a1 = data["a1_stability"].loc[data["a1_stability"]["scenario_id"].str.startswith("R2_")].copy()
    a1["model"] = "A1"
    h1 = data["h1_stability"].loc[data["h1_stability"]["scenario_id"].str.startswith("R2_")].copy()
    h1["model"] = "H5.1"
    return pd.concat([a1, h1], ignore_index=True)


def build_r7(data: Mapping[str, Any], config: FigureBuildConfig) -> Figure:
    """Build Figure R7: endpoint-preserving random-thinning robustness."""

    population = _random_population_rows(data)
    battery = data["random_battery"].loc[
        data["random_battery"]["scenario_id"].str.startswith("R2_")
    ]
    rank = data["random_summary"].loc[data["random_summary"]["scope"].eq("h1_per_battery_per_seed")]
    diagnostics = data["m8_diagnostics"]
    figure = _new_figure(config)
    axes = figure.subplots(2, 2)
    shift_axis, width_axis, rank_axis, battery_axis = axes.ravel()
    seeds = [20260616, 20260617, 20260618, 20260619]
    x = np.arange(len(seeds))

    for model, offset, color, marker in [
        ("A1", -0.08, BLUE["mid_highlight"], "s"),
        ("H5.1", 0.08, BLUE["dark_highlight"], "o"),
    ]:
        frame = population.loc[population["model"].eq(model)]
        for position, seed in enumerate(seeds):
            scenario = f"R2_random_keep_50_seed_{seed}"
            row = frame.loc[frame["scenario_id"].eq(scenario)].iloc[0]
            diagnostic = diagnostics.loc[
                diagnostics["scenario_id"].eq(scenario)
                & diagnostics["model_id"].eq(
                    "A1_bayesian_smooth_aggregate" if model == "A1" else "H1_hierarchical_h5_1"
                )
            ]
            accepted = bool(
                not diagnostic.empty and diagnostic.iloc[0]["diagnostic_status"] == "passed"
            )
            shift_axis.scatter(
                position + offset,
                row["tau_shift"],
                marker=marker,
                facecolors=color if accepted else "white",
                edgecolors=color,
                s=32,
                label=model if position == 0 else None,
            )
            width_axis.scatter(
                position + offset,
                row["tau_hdi_width_change_fraction"] + 1.0,
                marker=marker,
                facecolors=color if accepted else "white",
                edgecolors=color,
                s=32,
            )
    shift_axis.axhline(0, color=NEUTRAL["mid"], ls="--", lw=0.8)
    width_axis.axhline(1, color=NEUTRAL["mid"], ls="--", lw=0.8)
    rank_axis.plot(
        x,
        rank["rank_correlation_with_r0"],
        color=BLUE["dark"],
        marker="o",
        lw=1.1,
    )
    rank_axis.axhline(0.8, color=NEUTRAL["mid"], ls="--", lw=0.8)
    seed_styles = {
        20260616: ("o", "-"),
        20260617: ("s", "--"),
        20260618: ("^", "-."),
        20260619: ("D", ":"),
    }
    for scenario_id, frame in battery.groupby("scenario_id", sort=True):
        seed = int(scenario_id.rsplit("_", 1)[-1])
        seed_marker, seed_line_style = seed_styles[seed]
        battery_axis.plot(
            frame["battery_id"],
            frame["tau_shift_cycles"],
            marker=seed_marker,
            ls=seed_line_style,
            ms=2.8,
            lw=0.7,
            alpha=0.65,
            label=str(seed),
        )
    battery_axis.axhline(0, color=NEUTRAL["mid"], ls="--", lw=0.8)
    for axis in (shift_axis, width_axis, rank_axis):
        axis.set_xticks(x, [str(seed)[-2:] for seed in seeds])
        axis.set_xlabel("Mask seed suffix")
    shift_axis.set_ylabel("Midpoint shift (cycles)")
    width_axis.set_ylabel("95% HDI-width ratio")
    rank_axis.set_ylabel("H5.1 rank correlation")
    battery_axis.set_xlabel("Battery")
    battery_axis.set_xticks(range(1, 15))
    battery_axis.set_ylabel("H5.1 midpoint shift (cycles)")
    shift_axis.set_title("Population midpoint displacement")
    width_axis.set_title("Population uncertainty inflation")
    rank_axis.set_title("Battery-order stability")
    battery_axis.set_title("Battery-specific displacement")
    shift_axis.legend()
    battery_axis.legend(title="Seed", ncols=2, fontsize=6)
    for axis, label in zip(axes.ravel(), ["(a)", "(b)", "(c)", "(d)"], strict=True):
        _panel_label(axis, label)
        _clean_axis(axis)
    return figure


def build_r8(data: Mapping[str, Any], config: FigureBuildConfig) -> Figure:
    """Build Figure R8: trajectory-truncation sensitivity and predictive degradation."""

    table = data["truncation"].copy()
    diagnostics = data["m8_diagnostics"]
    figure = _new_figure(config)
    axes = figure.subplots(2, 2)
    shift_axis, rank_axis, rmse_axis, coverage_axis = axes.ravel()
    model_specs = [
        ("A1_bayesian_smooth_aggregate", "A1", BLUE["mid_highlight"], "s"),
        ("H1_hierarchical_h5_1", "H5.1", BLUE["dark_highlight"], "o"),
    ]
    for model_id, label, color, marker in model_specs:
        frame = table.loc[table["model_id"].eq(model_id)].sort_values("retained_fraction")
        shift_axis.plot(frame["retained_fraction"], frame["tau_shift"], color=color, lw=0.8)
        rmse_axis.plot(frame["retained_fraction"], frame["extrapolation_rmse"], color=color, lw=0.8)
        for _, row in frame.iterrows():
            diagnostic = diagnostics.loc[
                diagnostics["model_id"].eq(model_id)
                & diagnostics["scenario_id"].eq(row["scenario_id"])
            ]
            accepted = bool(
                not diagnostic.empty and diagnostic.iloc[0]["diagnostic_status"] == "passed"
            )
            special = model_id.startswith("A1") and np.isclose(row["retained_fraction"], 0.70)
            current_marker = "*" if special else marker
            shift_axis.scatter(
                row["retained_fraction"],
                row["tau_shift"],
                marker=current_marker,
                facecolors=color if accepted else "white",
                edgecolors=color,
                s=55 if special else 30,
                label=label
                if np.isclose(row["retained_fraction"], frame["retained_fraction"].min())
                else None,
                zorder=3,
            )
            rmse_axis.scatter(
                row["retained_fraction"],
                row["extrapolation_rmse"],
                marker=current_marker,
                facecolors=color if accepted else "white",
                edgecolors=color,
                s=55 if special else 30,
                zorder=3,
            )
            coverage_axis.scatter(
                row["retained_fraction"],
                row["posterior_predictive_coverage_90"],
                marker=marker,
                facecolors=color if accepted else "white",
                edgecolors=color,
                s=28,
            )
            coverage_axis.scatter(
                row["retained_fraction"],
                row["posterior_predictive_coverage_95"],
                marker=marker,
                facecolors="none",
                edgecolors=color,
                s=48,
            )
            if special:
                shift_axis.annotate(
                    "diagnostic only\n1 tree-depth saturation",
                    (row["retained_fraction"], row["tau_shift"]),
                    xytext=(-8, -25),
                    textcoords="offset points",
                    ha="right",
                    fontsize=6.5,
                )
        if model_id == "H1_hierarchical_h5_1":
            rank_axis.plot(
                frame["retained_fraction"],
                frame["tau_rank_correlation_with_r0"],
                color=color,
                marker=marker,
                lw=1.0,
            )
    shift_axis.axhline(0, color=NEUTRAL["mid"], ls="--", lw=0.8)
    rank_axis.axhline(0.8, color=NEUTRAL["mid"], ls="--", lw=0.8)
    coverage_axis.axhline(0.90, color=NEUTRAL["mid"], ls=":", lw=0.8)
    coverage_axis.axhline(0.95, color=NEUTRAL["dark"], ls=":", lw=0.8)
    for axis in axes.ravel():
        axis.set_xlabel("Retained trajectory fraction")
        axis.invert_xaxis()
        _clean_axis(axis)
    shift_axis.set_ylabel("Midpoint shift (cycles)")
    rank_axis.set_ylabel("H5.1 rank correlation")
    rmse_axis.set_ylabel("Extrapolation RMSE (C/D)")
    coverage_axis.set_ylabel("Predictive coverage")
    shift_axis.set_title("Population midpoint displacement")
    rank_axis.set_title("Battery-order stability")
    rmse_axis.set_title("Held-out extrapolation error")
    coverage_axis.set_title("90% and 95% coverage")
    shift_axis.legend()
    for axis, label in zip(axes.ravel(), ["(a)", "(b)", "(c)", "(d)"], strict=True):
        _panel_label(axis, label)
    return figure


def build_r9(data: Mapping[str, Any], config: FigureBuildConfig) -> Figure:
    """Build Figure R9: post-transition support against localization error and HDI ratio."""

    horizon = data["horizon"]
    classes = [
        "pre_transition",
        "transition_not_confirmed",
        "short_post_transition",
        "moderate_post_transition",
        "long_post_transition",
    ]
    markers = {
        "pre_transition": "X",
        "transition_not_confirmed": "D",
        "short_post_transition": "s",
        "moderate_post_transition": "^",
        "long_post_transition": "o",
    }
    figure = _new_figure(config)
    axes = figure.subplots(1, 2, sharex=True)
    left, right = axes
    for availability in classes:
        frame = horizon.loc[horizon["availability_class"].eq(availability)]
        left.scatter(
            frame["post_transition_horizon_cycles"],
            frame["absolute_tau_shift_cycles"],
            marker=markers[availability],
            facecolors=BLUE["mid"] if availability != "pre_transition" else YELLOW["dark"],
            edgecolors=NEUTRAL["dark"],
            s=34,
            alpha=0.8,
            label=availability.replace("_", " "),
        )
        right.scatter(
            frame["post_transition_horizon_cycles"],
            frame["tau_hdi_width_ratio"],
            marker=markers[availability],
            facecolors=BLUE["mid"] if availability != "pre_transition" else YELLOW["dark"],
            edgecolors=NEUTRAL["dark"],
            s=34,
            alpha=0.8,
            label=availability.replace("_", " "),
        )
    battery_11 = horizon.loc[horizon["battery_id"].eq(11)]
    left_annotation_offsets = {
        0.90: (5, -10),
        0.80: (5, 4),
        0.75: (5, -12),
        0.70: (5, -11),
        0.60: (5, 4),
    }
    right_annotation_offsets = {
        0.90: (10, -14),
        0.80: (10, 8),
        0.75: (10, 8),
        0.70: (10, -14),
        0.60: (10, 8),
    }
    for axis, y_column in [
        (left, "absolute_tau_shift_cycles"),
        (right, "tau_hdi_width_ratio"),
    ]:
        offsets = (
            left_annotation_offsets
            if y_column == "absolute_tau_shift_cycles"
            else right_annotation_offsets
        )
        for _, row in battery_11.iterrows():
            retained_fraction = round(float(row["retained_fraction"]), 2)
            retained_percent = round(retained_fraction * 100)
            point_label = (
                f"B11 {retained_percent}%"
                if y_column == "absolute_tau_shift_cycles"
                else f"{retained_percent}%"
            )
            axis.annotate(
                point_label,
                (row["post_transition_horizon_cycles"], row[y_column]),
                xytext=offsets[retained_fraction],
                textcoords="offset points",
                fontsize=6,
                color=NEUTRAL["near_black"],
            )
    rho_shift = float(horizon["spearman_tau_shift"].iloc[0])
    rho_width = float(horizon["spearman_hdi_inflation"].iloc[0])
    left.text(
        0.97,
        0.96,
        rf"Spearman $\rho={rho_shift:.2f}$",
        transform=left.transAxes,
        ha="right",
        va="top",
    )
    right.text(
        0.03,
        0.96,
        rf"Spearman $\rho={rho_width:.2f}$",
        transform=right.transAxes,
        va="top",
    )
    left.set_xlabel("Post-transition horizon (cycles)")
    right.set_xlabel("Post-transition horizon (cycles)")
    left.set_ylabel("Absolute midpoint shift (cycles)")
    right.set_ylabel("95% HDI-width ratio")
    left.set_title("Localization displacement")
    right.set_title("Interval-width change")
    right.text(
        0.03,
        0.87,
        "Battery 11 labels: retained fraction",
        transform=right.transAxes,
        va="top",
        fontsize=6,
    )
    right.legend(fontsize=6, loc="upper right")
    _panel_label(left, "(a)")
    _panel_label(right, "(b)")
    _clean_axis(left)
    _clean_axis(right)
    return figure


def build_r10(data: Mapping[str, Any], config: FigureBuildConfig) -> Figure:
    """Build Figure R10: Battery 11 full-data and truncation localization case."""

    trajectory = data["ppc_trajectory"].loc[data["ppc_trajectory"]["Battery_ID"].eq(11)]
    full = data["h5_battery"].set_index("Battery_ID").loc[11]
    scenarios = data["truncation_battery"].loc[
        data["truncation_battery"]["Battery_ID"].eq(11)
        & data["truncation_battery"]["scenario_id"].str.startswith("R4_")
    ]
    masks = data["mask_registry"].loc[
        data["mask_registry"]["battery_id"].eq(11)
        & data["mask_registry"]["scenario_id"].str.startswith("R4_")
    ]
    common_width = float(
        data["h5_population"].set_index("quantity").loc["shared_transition_width_cycles", "median"]
    )
    order = [
        "R0_full",
        "R4_truncate_90",
        "R4_truncate_80",
        "R4_truncate_75",
        "R4_truncate_70",
        "R4_truncate_60",
    ]
    figure = _new_figure(config)
    axes = figure.subplots(2, 3, sharex=True, sharey=True)
    for axis, scenario_id in zip(axes.ravel(), order, strict=True):
        if scenario_id == "R0_full":
            observed_end = float(trajectory["cycle_original"].max())
            scenario_tau = float(full["tau_median_cycles"])
            title = "Full trajectory"
        else:
            observed_end = float(
                masks.loc[masks["scenario_id"].eq(scenario_id), "observed_cycle_max"].iloc[0]
            )
            scenario_tau = float(
                scenarios.loc[scenarios["scenario_id"].eq(scenario_id), "tau_median"].iloc[0]
            )
            title = f"{scenario_id.rsplit('_', 1)[-1]}% retained"
        observed = trajectory["cycle_original"].le(observed_end)
        axis.scatter(
            trajectory.loc[observed, "cycle_original"],
            trajectory.loc[observed, "observed_response"],
            s=4,
            color=NEUTRAL["mid"],
            alpha=0.38,
            rasterized=True,
        )
        if (~observed).any():
            axis.scatter(
                trajectory.loc[~observed, "cycle_original"],
                trajectory.loc[~observed, "observed_response"],
                s=4,
                facecolors="none",
                edgecolors=NEUTRAL["light"],
                linewidths=0.35,
                rasterized=True,
            )
            axis.axvspan(
                observed_end, trajectory["cycle_original"].max(), color=NEUTRAL["light"], alpha=0.14
            )
        axis.fill_between(
            trajectory["cycle_original"],
            trajectory["latent_mean_90_lower"],
            trajectory["latent_mean_90_upper"],
            color=BLUE["light_highlight"],
            alpha=0.55,
        )
        axis.plot(
            trajectory["cycle_original"],
            trajectory["latent_mean_median"],
            color=BLUE["dark"],
            lw=1.0,
        )
        axis.axvline(full["tau_median_cycles"], color=BLUE["dark_highlight"], ls="--", lw=0.9)
        axis.axvline(scenario_tau, color=YELLOW["dark_highlight"], ls="-.", lw=1.1)
        axis.set_title(title)
        _clean_axis(axis)
        if scenario_id == "R4_truncate_90":
            horizon = observed_end - float(full["tau_median_cycles"])
            axis.text(
                0.03,
                0.96,
                f"post-transition horizon = {horizon:.0f} cycles\ncommon width = {common_width:.0f} cycles",
                transform=axis.transAxes,
                ha="left",
                va="top",
                fontsize=6.5,
            )
    figure.supxlabel("Cycle index")
    figure.supylabel("C/D")
    return figure


FIGURE_BUILDERS: dict[str, Callable[[Mapping[str, Any], FigureBuildConfig], Figure]] = {
    "results-cd-trajectories": build_r1,
    "results-transition-definitions": build_r2,
    "results-h5-transition-midpoints": build_r3,
    "results-h5-slope-acceleration": build_r4,
    "results-h5-selected-fits": build_r5,
    "results-h5-ppc": build_r6,
    "results-random-thinning": build_r7,
    "results-truncation-sensitivity": build_r8,
    "results-post-transition-horizon": build_r9,
    "results-battery11-truncation": build_r10,
}
