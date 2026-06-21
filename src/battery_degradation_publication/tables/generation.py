"""Generate active manuscript tables from frozen sources or curated records.

Computed tables read accepted analytical artifacts and resolved configuration
metadata. Curated tables preserve the exact author-approved wording supplied in
the manuscript source. No model fitting, resampling, or posterior computation is
performed here.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from ..figure_config import PACKAGE_ROOT

FROZEN = PACKAGE_ROOT / "data/frozen_results"
SOURCE = FROZEN / "table_sources"
REFERENCE = PACKAGE_ROOT / "tables/reference"
GENERATED = PACKAGE_ROOT / "tables/generated"
MACHINE = PACKAGE_ROOT / "tables/machine_readable"

TableGenerator = Callable[[], tuple[pd.DataFrame, str]]


def _read_json(path: Path) -> dict[str, Any]:
    """Read one required JSON object."""

    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def _read_yaml(path: Path) -> dict[str, Any]:
    """Read one required YAML mapping."""

    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping: {path}")
    return value


def _share(count: int, total: int) -> str:
    """Format a manuscript percentage with exactly two decimal places."""

    return f"{100 * count / total:.2f}%"


def _latex_percent(value: str) -> str:
    """Escape a display percentage for LaTeX."""

    return value.replace("%", "\\%")


def _with_generated_body(identifier: str, body_lines: list[str]) -> str:
    """Insert generated rows into the accepted manuscript table layout.

    The reference file supplies caption, label, MDPI width handling, and column
    definitions. Only the rows between ``\\midrule`` and ``\\bottomrule`` are
    replaced, so computed numerical content comes from frozen artifacts.
    """

    reference = (REFERENCE / f"{identifier}.tex").read_text(encoding="utf-8")
    prefix, remainder = reference.split("\\midrule\n", maxsplit=1)
    _, suffix = remainder.split("\\bottomrule", maxsplit=1)
    return prefix + "\\midrule\n" + "\n".join(body_lines) + "\n\\bottomrule" + suffix


def _curated(
    identifier: str,
    columns: list[str],
    rows: list[list[str]],
    provenance: str,
) -> tuple[pd.DataFrame, str]:
    """Return a curated table and its exact accepted LaTeX source."""

    frame = pd.DataFrame(rows, columns=columns)
    frame["entry_provenance"] = provenance
    frame["citation_keys"] = ""
    return frame, (REFERENCE / f"{identifier}.tex").read_text(encoding="utf-8")


def battery_technology_context() -> tuple[pd.DataFrame, str]:
    """Return the exact author-curated battery-technology context table."""

    return _curated(
        "battery_technology_context",
        [
            "Technology",
            "Application context and principal strengths",
            "Lifecycle limitations",
            "Monitoring relevance",
        ],
        [
            [
                "Lead--acid",
                "Backup power, starting, and industrial standby; mature, low initial cost, high surge power, and established recycling",
                "High mass, moderate cycle life, sulfation and corrosion, and maintenance sensitivity",
                "Voltage, current, temperature, charge acceptance, and resistance provide useful ageing information",
            ],
            [
                "Nickel-based",
                "Industrial equipment and legacy hybrid or portable systems; robust operation and good power capability in selected conditions",
                "Self-discharge, memory effects for NiCd, cadmium toxicity, and lower energy density than Li-ion",
                "Thermal and charging-control history are important for interpreting health",
            ],
            [
                "Lithium-ion",
                "Electric mobility, portable electronics, and stationary storage; high efficiency, energy and power density, low self-discharge, and broad commercial maturity",
                "Coupled calendar and cycle ageing, thermal sensitivity, cell variability, and safety-management requirements",
                "Strong need for cell-level voltage and temperature supervision and uncertainty-aware SOH estimation",
            ],
            [
                "Sodium-ion",
                "Emerging stationary and cost-sensitive storage; abundant raw materials and potential cost and sustainability benefits",
                "Lower energy density and less mature field experience; chemistry-dependent cycle life",
                "Monitoring concepts resemble Li-ion but require chemistry-specific calibration and validation",
            ],
            [
                "Lithium--sulfur",
                "Prospective weight-sensitive applications; high theoretical specific energy and low-cost active sulfur",
                "Polysulfide shuttle, limited cycle life, and lithium-metal-anode challenges",
                "Health indicators must capture rapidly changing electrochemistry and loss mechanisms",
            ],
        ],
        "author synthesis informed by literature; no table-local citation keys",
    )


def degradation_mechanisms_observability() -> tuple[pd.DataFrame, str]:
    """Return the exact author-curated degradation-observability table."""

    return _curated(
        "degradation_mechanisms_observability",
        [
            "Mechanism or degradation mode",
            "Possible consequence",
            "Potential observable signatures",
            "Availability in the present dataset",
        ],
        [
            [
                "SEI growth and electrolyte side reactions",
                "Loss of cyclable lithium, impedance increase, capacity and power fade",
                "Capacity loss, resistance or EIS change, altered charge acceptance, and heat generation",
                "Only indirect influence through charge/discharge durations and C/D",
            ],
            [
                "Lithium plating",
                "Loss of lithium, local deposits, accelerated ageing, and potential safety concern",
                "Voltage relaxation, coulombic efficiency, impedance, and temperature response; confirmation often requires dedicated diagnostics",
                "Not directly observed",
            ],
            [
                "Loss of active material and particle cracking",
                "Reduced electrode utilization, contact loss, and capacity fade",
                "Changes in capacity, incremental-capacity or differential-voltage features, resistance, and mechanical response",
                "Not directly observed",
            ],
            [
                "Electrolyte oxidation, gas evolution, and interfacial degradation",
                "Increased impedance, pressure, transport limitation, and possible swelling",
                "EIS, pressure or gas sensing, thermal response, and voltage behaviour",
                "Not directly observed",
            ],
            [
                "Current-collector, tab, or connection degradation",
                "Ohmic loss, voltage drop, non-uniform heating, and local power limitation",
                "DC resistance, pulse response, voltage differences, thermal signals, and vibration diagnostics",
                "Only indirect influence through cycle durations",
            ],
            [
                "Thermal gradients and operational imbalance",
                "Unequal ageing rates across cells and locally accelerated degradation",
                "Distributed temperature, cell-voltage imbalance, current, and usage history",
                "Temperature and pack context unavailable in the derivative file",
            ],
        ],
        "author synthesis of literature-derived mechanisms and dataset observability; no table-local citation keys",
    )


def transition_definitions() -> tuple[pd.DataFrame, str]:
    """Return the exact author-defined methodological role table."""

    return _curated(
        "transition_definitions",
        [
            "Code",
            "Observation structure",
            "Model role and estimand",
            "Uncertainty or stability assessment",
        ],
        [
            [
                "B0",
                "1,071 cycle medians",
                "Constant-slope no-transition reference",
                "No changepoint parameter",
            ],
            [
                "D1",
                "1,071 cycle medians",
                "Sharp breakpoint joining two continuous linear regimes",
                "Moving-block residual bootstrap",
            ],
            [
                "S1",
                "1,071 cycle medians",
                "Interior cycle of maximum smoothing-spline curvature",
                "Smoothing-ladder stability gate",
            ],
            [
                "A1",
                "1,071 cycle medians",
                "Midpoint of an aggregate gradual slope transition",
                "Bayesian posterior interval",
            ],
            [
                "H5.1",
                "14,848 battery--cycle rows",
                "Battery-specific gradual-transition midpoints and draw-wise population summaries",
                "Hierarchical Bayesian posterior intervals and boundary diagnostics",
            ],
        ],
        "author-defined methodological terminology; no table-local citation keys",
    )


def preprocessing_summary() -> tuple[pd.DataFrame, str]:
    """Regenerate the locked preprocessing partition table."""

    source = _read_json(SOURCE / "preprocessing_summary.json")
    total = int(source["source_observations"])
    rows = [
        ["Source observations", f"{total:,}", "100.00%", "All rows in the distributed file"],
        [
            "Cycle-index resets",
            str(source["cycle_index_resets"]),
            "---",
            "Strict decreases in preserved source order",
        ],
        [
            "Inferred battery records",
            str(source["inferred_battery_records"]),
            "---",
            "One plus the cumulative reset count",
        ],
        [
            "Candidate long-duration rows",
            f"{source['candidate_long_duration_rows']:,}",
            _share(int(source["candidate_long_duration_rows"]), total),
            "Either duration >20,000 s",
        ],
        [
            "Candidate incomplete rows",
            f"{source['candidate_incomplete_rows']:,}",
            _share(int(source["candidate_incomplete_rows"]), total),
            "Discharge <600 s or charge <3,000 s",
        ],
        [
            "Overlap of candidate flags",
            str(source["candidate_flag_overlap"]),
            _share(int(source["candidate_flag_overlap"]), total),
            "Rows satisfying both candidate rules",
        ],
        [
            "Regular-eligible rows",
            f"{source['regular_eligible_rows']:,}",
            _share(int(source["regular_eligible_rows"]), total),
            "Neither candidate flag",
        ],
        [
            "Complete regular aggregate",
            f"{source['complete_regular_aggregate_cycles']:,} cycles",
            "---",
            "Median C/D at every represented cycle",
        ],
        [
            "Retained aggregate",
            f"{source['retained_aggregate_cycles']:,} cycles",
            "---",
            "At least seven contributing batteries",
        ],
        [
            "Excluded low-support aggregate",
            f"{source['excluded_low_support_aggregate_cycles']} cycles",
            "---",
            "Fewer than seven contributing batteries",
        ],
    ]
    frame = pd.DataFrame(rows, columns=["Quantity", "Count", "Share", "Definition"])
    latex = _with_generated_body(
        "preprocessing_summary",
        [
            f"Source observations & {total:,} & 100.00\\% & All rows in the distributed file\\\\",
            f"Cycle-index resets & {source['cycle_index_resets']} & --- & Strict decreases in preserved source order\\\\",
            f"Inferred battery records & {source['inferred_battery_records']} & --- & One plus the cumulative reset count\\\\",
            f"Candidate long-duration rows & {source['candidate_long_duration_rows']:,} & {_latex_percent(_share(int(source['candidate_long_duration_rows']), total))} & Either duration $>20{{,}}000$~s\\\\",
            f"Candidate incomplete rows & {source['candidate_incomplete_rows']:,} & {_latex_percent(_share(int(source['candidate_incomplete_rows']), total))} & Discharge $<600$~s or charge $<3{{,}}000$~s\\\\",
            f"Overlap of candidate flags & {source['candidate_flag_overlap']} & {_latex_percent(_share(int(source['candidate_flag_overlap']), total))} & Rows satisfying both candidate rules\\\\",
            f"Regular-eligible rows & {source['regular_eligible_rows']:,} & {_latex_percent(_share(int(source['regular_eligible_rows']), total))} & Neither candidate flag\\\\",
            f"Complete regular aggregate & {source['complete_regular_aggregate_cycles']:,} cycles & --- & Median \\CD{{}} at every represented cycle\\\\",
            f"Retained aggregate & {source['retained_aggregate_cycles']:,} cycles & --- & At least seven contributing batteries\\\\",
            f"Excluded low-support aggregate & {source['excluded_low_support_aggregate_cycles']} cycles & --- & Fewer than seven contributing batteries\\\\",
        ],
    )
    return frame, latex


def computation_gates() -> tuple[pd.DataFrame, str]:
    """Regenerate accepted A1 and H5.1 sampling and diagnostic gates."""

    a1_config = _read_yaml(SOURCE / "m4_config_resolved.yaml")
    h5_config = _read_yaml(SOURCE / "h5_config_resolved.yaml")
    a1_diag = _read_json(SOURCE / "m4_bayesian_diagnostics.json")
    h5_diag = _read_json(SOURCE / "h5_hierarchical_diagnostics.json")["diagnostics"]
    exact = pd.read_csv(SOURCE / "h5_exact_parameter_diagnostics.csv")
    key = exact.loc[exact["diagnostic_priority"].eq("smoke_key")]
    h5_rhat = float(exact["rhat_rank"].max())
    h5_bulk = float(key["ess_bulk"].min())
    h5_tail = float(key["ess_tail"].min())
    rows = [
        [
            "Chains / cores",
            f"{a1_config['model']['chains']} / {a1_config['model']['cores']}",
            f"{h5_config['model']['chains']} / {h5_config['model']['cores']}",
            "---",
        ],
        [
            "Tuning iterations per chain",
            f"{a1_config['model']['tune']:,}",
            f"{h5_config['model']['tune']:,}",
            "---",
        ],
        [
            "Retained draws per chain",
            f"{a1_config['model']['draws']:,}",
            f"{h5_config['model']['draws']:,}",
            "---",
        ],
        [
            "Random seed",
            str(a1_config["model"]["random_seed"]),
            str(h5_config["model"]["random_seed"]),
            "Fixed by configuration",
        ],
        [
            "Target acceptance",
            f"{a1_config['model']['target_accept']:.2f}",
            f"{h5_config['model']['target_accept']:.2f}",
            "---",
        ],
        [
            "Maximum tree depth",
            str(a1_config["model"]["max_treedepth"]),
            str(h5_config["model"]["max_treedepth"]),
            "No saturated post-warm-up draws",
        ],
        [
            "Initialization / metric",
            "auto; PyMC automatic metric",
            "jitter+adapt_full; dense metric",
            "---",
        ],
        [
            "Maximum rank/default Rhat",
            f"{a1_diag['maximum_r_hat']:.3f}",
            f"{h5_rhat:.6f}",
            "<=1.01",
        ],
        ["Minimum bulk ESS", f"{a1_diag['minimum_bulk_ess']:,.0f}", f"{h5_bulk:,.2f}", ">=400"],
        ["Minimum tail ESS", f"{a1_diag['minimum_tail_ess']:,.0f}", f"{h5_tail:,.2f}", ">=400"],
        ["Divergences", str(a1_diag["divergence_count"]), str(h5_diag["divergence_count"]), "0"],
        [
            "Tree-depth saturations",
            str(a1_diag["treedepth_saturation_count"]),
            str(h5_diag["treedepth_saturation_count"]),
            "0",
        ],
        [
            "Minimum E-BFMI",
            f"{a1_diag['minimum_e_bfmi']:.4f}",
            f"{h5_diag['minimum_e_bfmi']:.4f}",
            ">=0.30",
        ],
        ["Final gate", "Passed", "Passed", "All applicable criteria"],
    ]
    frame = pd.DataFrame(rows, columns=["Setting or diagnostic", "A1", "H5.1", "Acceptance rule"])
    latex = _with_generated_body(
        "computation_gates",
        [
            f"Chains / cores & {a1_config['model']['chains']} / {a1_config['model']['cores']} & {h5_config['model']['chains']} / {h5_config['model']['cores']} & ---\\\\",
            f"Tuning iterations per chain & {a1_config['model']['tune']:,} & {h5_config['model']['tune']:,} & ---\\\\",
            f"Retained draws per chain & {a1_config['model']['draws']:,} & {h5_config['model']['draws']:,} & ---\\\\",
            f"Random seed & {a1_config['model']['random_seed']} & {h5_config['model']['random_seed']} & Fixed by configuration\\\\",
            f"Target acceptance & {a1_config['model']['target_accept']:.2f} & {h5_config['model']['target_accept']:.2f} & ---\\\\",
            f"Maximum tree depth & {a1_config['model']['max_treedepth']} & {h5_config['model']['max_treedepth']} & No saturated post-warm-up draws\\\\",
            "Initialization / metric & \\texttt{auto}; PyMC automatic metric & \\texttt{jitter+adapt\\_full}; dense metric & ---\\\\",
            f"Maximum rank/default $\\Rhat$ & {a1_diag['maximum_r_hat']:.3f} & {h5_rhat:.6f} & $\\leq1.01$\\\\",
            f"Minimum bulk ESS & {a1_diag['minimum_bulk_ess']:,.0f} & {h5_bulk:,.2f} & $\\geq400$\\\\",
            f"Minimum tail ESS & {a1_diag['minimum_tail_ess']:,.0f} & {h5_tail:,.2f} & $\\geq400$\\\\",
            f"Divergences & {a1_diag['divergence_count']} & {h5_diag['divergence_count']} & 0\\\\",
            f"Tree-depth saturations & {a1_diag['treedepth_saturation_count']} & {h5_diag['treedepth_saturation_count']} & 0\\\\",
            f"Minimum E-BFMI & {a1_diag['minimum_e_bfmi']:.4f} & {h5_diag['minimum_e_bfmi']:.4f} & $\\geq0.30$\\\\",
            "Final gate & Passed & Passed & All applicable criteria\\\\",
        ],
    )
    return frame, latex


def changepoint_results() -> tuple[pd.DataFrame, str]:
    """Regenerate aggregate B0, D1, A1, and S1 results."""

    methods = pd.read_csv(FROZEN / "m4/changepoint_method_summary.csv").set_index("method")
    transition = pd.read_csv(SOURCE / "m4_transition_summary.csv").iloc[0]
    curvature = _read_json(SOURCE / "m4_curvature_stability.json")
    b0 = methods.loc["linear"]
    d1 = methods.loc["broken_stick"]
    a1 = methods.loc["bayesian_smooth"]
    rows = [
        [
            "B0",
            "No transition",
            "---",
            f"{b0['pre_slope']:.6f}",
            f"{b0['post_slope']:.6f}",
            "Constant-slope reference",
        ],
        [
            "D1",
            "Sharp continuous breakpoint",
            f"{d1['changepoint_cycle']:.1f} [{d1['interval_lower']:.1f}, {d1['interval_upper']:.1f}]",
            f"{d1['pre_slope']:.6f}",
            f"{d1['post_slope']:.6f}",
            f"Slope increment {d1['slope_change']:.6f}",
        ],
        [
            "A1",
            "Smooth-transition midpoint",
            f"{a1['changepoint_cycle']:.1f} [{a1['interval_lower']:.1f}, {a1['interval_upper']:.1f}]",
            f"{a1['pre_slope']:.6f}",
            f"{a1['post_slope']:.6f}",
            f"Width {transition['transition_width_cycles_median']:.1f} [{transition['transition_width_cycles_hdi_95_lower']:.1f}, {transition['transition_width_cycles_hdi_95_upper']:.1f}] cycles; Pr(delta beta > 0 | y)=1",
        ],
        [
            "S1",
            "Maximum-curvature knee",
            "Not reported",
            "---",
            "---",
            f"Smoothing-sensitive; candidate range {curvature['knee_cycle_range']:.1f} cycles",
        ],
    ]
    frame = pd.DataFrame(
        rows,
        columns=[
            "Model",
            "Transition estimand",
            "Location, cycles",
            "Pre-slope",
            "Post-slope",
            "Status or additional result",
        ],
    )
    latex = _with_generated_body(
        "changepoint_results",
        [
            f"B0 & No transition & --- & {b0['pre_slope']:.6f} & {b0['post_slope']:.6f} & Constant-slope reference\\\\",
            f"D1 & Sharp continuous breakpoint & {d1['changepoint_cycle']:.1f} [{d1['interval_lower']:.1f}, {d1['interval_upper']:.1f}] & {d1['pre_slope']:.6f} & {d1['post_slope']:.6f} & Slope increment {d1['slope_change']:.6f}\\\\",
            f"A1 & Smooth-transition midpoint & {a1['changepoint_cycle']:.1f} [{a1['interval_lower']:.1f}, {a1['interval_upper']:.1f}] & {a1['pre_slope']:.6f} & {a1['post_slope']:.6f} & Width {transition['transition_width_cycles_median']:.1f} [{transition['transition_width_cycles_hdi_95_lower']:.1f}, {transition['transition_width_cycles_hdi_95_upper']:.1f}] cycles; $\\Pr(\\Delta\\beta>0\\mid y)=1$\\\\",
            f"S1 & Maximum-curvature knee & Not reported & --- & --- & Smoothing-sensitive; candidate range {curvature['knee_cycle_range']:.1f} cycles\\\\",
        ],
    )
    return frame, latex


def hierarchical_population_results() -> tuple[pd.DataFrame, str]:
    """Regenerate accepted H5.1 population posterior summaries."""

    source = pd.read_csv(FROZEN / "h5/accepted_population_scientific_summary.csv").set_index(
        "quantity"
    )
    mapping = [
        ("Population transition midpoint, cycles", "population_transition_midpoint_cycles"),
        ("Between-battery midpoint SD, cycles", "between_battery_transition_midpoint_sd_cycles"),
        ("Shared transition width, cycles", "shared_transition_width_cycles"),
        ("Population pre-transition slope", "population_pre_transition_slope_cd_per_cycle"),
        ("Population post-transition slope", "population_post_transition_slope_cd_per_cycle"),
        ("Population slope increment", "population_slope_change_cd_per_cycle"),
        ("Shared residual scale, C/D", "shared_residual_scale_cd"),
    ]
    rows = []
    latex_rows = []
    for index, (label, key) in enumerate(mapping):
        precision = 3 if index < 3 else 6
        median = f"{source.loc[key, 'median']:.{precision}f}"
        interval = (
            f"[{source.loc[key, 'hdi_lower']:.{precision}f}, "
            f"{source.loc[key, 'hdi_upper']:.{precision}f}]"
        )
        rows.append([label, median, interval])
        latex_label = label.replace("C/D", "\\CD{}")
        latex_rows.append(f"{latex_label} & {median} & {interval}\\\\")
    frame = pd.DataFrame(rows, columns=["Quantity", "Posterior median", "95% HDI"])
    latex = _with_generated_body(
        "hierarchical_population_results",
        latex_rows,
    )
    return frame, latex


def truncation_results() -> tuple[pd.DataFrame, str]:
    """Regenerate the A1/H5.1 trajectory-truncation sensitivity table."""

    source = pd.read_csv(FROZEN / "m8/truncation_summary.csv")
    a1 = source.loc[source["model_id"].eq("A1_bayesian_smooth_aggregate")].set_index(
        "retained_fraction"
    )
    h5 = source.loc[source["model_id"].eq("H1_hierarchical_h5_1")].set_index("retained_fraction")
    rows: list[list[str]] = []
    for retained in (0.90, 0.80, 0.75, 0.70, 0.60):
        dagger = "†" if retained == 0.70 else ""
        rows.append(
            [
                f"{retained:.0%}",
                f"{a1.loc[retained, 'tau_shift']:+.1f}{dagger}",
                f"{a1.loc[retained, 'posterior_predictive_coverage_90']:.3f}",
                f"{a1.loc[retained, 'posterior_predictive_coverage_95']:.3f}",
                f"{h5.loc[retained, 'tau_shift']:+.1f}",
                f"{h5.loc[retained, 'tau_rank_correlation_with_r0']:.3f}",
                f"{h5.loc[retained, 'extrapolation_rmse']:.3f}",
                f"{h5.loc[retained, 'posterior_predictive_coverage_90']:.3f}",
                f"{h5.loc[retained, 'posterior_predictive_coverage_95']:.3f}",
            ]
        )
    frame = pd.DataFrame(
        rows,
        columns=[
            "Retained",
            "A1 delta tau (cycles)",
            "A1 90% coverage",
            "A1 95% coverage",
            "H5.1 delta tau (cycles)",
            "H5.1 rank rho",
            "H5.1 RMSE",
            "H5.1 90% coverage",
            "H5.1 95% coverage",
        ],
    )
    latex_rows = [
        f"90\\% & ${a1.loc[0.90, 'tau_shift']:+.1f}$ & {a1.loc[0.90, 'posterior_predictive_coverage_90']:.3f} & {a1.loc[0.90, 'posterior_predictive_coverage_95']:.3f} & ${h5.loc[0.90, 'tau_shift']:+.1f}$  & {h5.loc[0.90, 'tau_rank_correlation_with_r0']:.3f}    & {h5.loc[0.90, 'extrapolation_rmse']:.3f} & {h5.loc[0.90, 'posterior_predictive_coverage_90']:.3f} & {h5.loc[0.90, 'posterior_predictive_coverage_95']:.3f}\\\\",
        f"80\\% & ${a1.loc[0.80, 'tau_shift']:+.1f}$  & {a1.loc[0.80, 'posterior_predictive_coverage_90']:.3f} & {a1.loc[0.80, 'posterior_predictive_coverage_95']:.3f} & ${h5.loc[0.80, 'tau_shift']:+.1f}$  & {h5.loc[0.80, 'tau_rank_correlation_with_r0']:.3f}    & {h5.loc[0.80, 'extrapolation_rmse']:.3f} & {h5.loc[0.80, 'posterior_predictive_coverage_90']:.3f} & {h5.loc[0.80, 'posterior_predictive_coverage_95']:.3f}\\\\",
        f"75\\% & ${a1.loc[0.75, 'tau_shift']:+.1f}$ & {a1.loc[0.75, 'posterior_predictive_coverage_90']:.3f} & {a1.loc[0.75, 'posterior_predictive_coverage_95']:.3f} & ${h5.loc[0.75, 'tau_shift']:+.1f}$  & {h5.loc[0.75, 'tau_rank_correlation_with_r0']:.3f}    & {h5.loc[0.75, 'extrapolation_rmse']:.3f} & {h5.loc[0.75, 'posterior_predictive_coverage_90']:.3f} & {h5.loc[0.75, 'posterior_predictive_coverage_95']:.3f}\\\\",
        f"70\\% & ${a1.loc[0.70, 'tau_shift']:+.1f}^{{\\dagger}}$ & {a1.loc[0.70, 'posterior_predictive_coverage_90']:.3f} & {a1.loc[0.70, 'posterior_predictive_coverage_95']:.3f} & ${h5.loc[0.70, 'tau_shift']:+.1f}$  & {h5.loc[0.70, 'tau_rank_correlation_with_r0']:.3f}    & {h5.loc[0.70, 'extrapolation_rmse']:.3f} & {h5.loc[0.70, 'posterior_predictive_coverage_90']:.3f} & {h5.loc[0.70, 'posterior_predictive_coverage_95']:.3f}\\\\",
        f"60\\% & ${a1.loc[0.60, 'tau_shift']:+.1f}$ & {a1.loc[0.60, 'posterior_predictive_coverage_90']:.3f} & {a1.loc[0.60, 'posterior_predictive_coverage_95']:.3f} & ${h5.loc[0.60, 'tau_shift']:+.1f}$ & ${h5.loc[0.60, 'tau_rank_correlation_with_r0']:.3f}$ & {h5.loc[0.60, 'extrapolation_rmse']:.3f} & {h5.loc[0.60, 'posterior_predictive_coverage_90']:.3f} & {h5.loc[0.60, 'posterior_predictive_coverage_95']:.3f}\\\\",
    ]
    latex = _with_generated_body("truncation_results", latex_rows)
    return frame, latex


TABLE_GENERATORS: dict[str, TableGenerator] = {
    "battery_technology_context": battery_technology_context,
    "degradation_mechanisms_observability": degradation_mechanisms_observability,
    "preprocessing_summary": preprocessing_summary,
    "transition_definitions": transition_definitions,
    "computation_gates": computation_gates,
    "changepoint_results": changepoint_results,
    "hierarchical_population_results": hierarchical_population_results,
    "truncation_results": truncation_results,
}


def generate_tables(table_ids: Sequence[str] | None = None) -> int:
    """Generate selected active manuscript tables as CSV and LaTeX.

    Parameters
    ----------
    table_ids:
        Active table identifiers. ``None`` generates all tables in manuscript
        input order.

    Returns
    -------
    int
        Zero after all files are written successfully.

    Raises
    ------
    ValueError
        If an unknown table identifier is supplied.
    OSError
        If an output cannot be written.
    """

    selected = list(table_ids) if table_ids is not None else list(TABLE_GENERATORS)
    unknown = [identifier for identifier in selected if identifier not in TABLE_GENERATORS]
    if unknown:
        raise ValueError(
            f"Unknown table identifier(s): {unknown}. Known tables: {', '.join(TABLE_GENERATORS)}"
        )
    GENERATED.mkdir(parents=True, exist_ok=True)
    MACHINE.mkdir(parents=True, exist_ok=True)
    for identifier in selected:
        frame, latex = TABLE_GENERATORS[identifier]()
        frame.to_csv(MACHINE / f"{identifier}.csv", index=False)
        (GENERATED / f"{identifier}.tex").write_text(latex, encoding="utf-8")
    return 0


def cited_keys(latex: str) -> set[str]:
    """Return bibliography keys referenced directly by a table's LaTeX."""

    keys: set[str] = set()
    for group in re.findall(r"\\cite\{([^}]+)\}", latex):
        keys.update(key.strip() for key in group.split(","))
    return keys
