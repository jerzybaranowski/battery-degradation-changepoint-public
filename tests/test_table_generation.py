"""Tests for active manuscript-table generation and validation."""

from pathlib import Path

import pandas as pd
import pytest
from battery_degradation_publication.figure_config import PACKAGE_ROOT
from battery_degradation_publication.tables import TABLE_GENERATORS, generate_tables

EXPECTED_TABLES = [
    "battery_technology_context",
    "degradation_mechanisms_observability",
    "preprocessing_summary",
    "transition_definitions",
    "computation_gates",
    "changepoint_results",
    "hierarchical_population_results",
    "truncation_results",
]


def test_active_table_registry_matches_manuscript_inputs() -> None:
    """The generator registry must contain exactly the eight active tables."""

    assert list(TABLE_GENERATORS) == EXPECTED_TABLES


@pytest.mark.parametrize("table_id", EXPECTED_TABLES)
def test_generated_latex_matches_active_manuscript_source(table_id: str) -> None:
    """Generated manuscript LaTeX must be byte-identical to its active source."""

    frame, latex = TABLE_GENERATORS[table_id]()
    assert not frame.empty
    reference = PACKAGE_ROOT / "tables/reference" / f"{table_id}.tex"
    assert latex == reference.read_text(encoding="utf-8")
    assert all(token not in latex for token in (r"\footnotesize", r"\scriptsize", r"\resizebox"))


def test_generated_hierarchical_population_precision() -> None:
    """Cycle summaries use three decimals and slope summaries use six."""

    frame, _ = TABLE_GENERATORS["hierarchical_population_results"]()
    assert frame.iloc[0]["Posterior median"] == "553.872"
    assert frame.iloc[3]["Posterior median"] == "0.000947"


def test_truncation_dagger_and_negative_rank_are_preserved() -> None:
    """The diagnostic-only A1 result and negative H5.1 rank must remain explicit."""

    frame, latex = TABLE_GENERATORS["truncation_results"]()
    row_70 = frame.loc[frame["Retained"].eq("70%")].iloc[0]
    row_60 = frame.loc[frame["Retained"].eq("60%")].iloc[0]
    assert row_70["A1 delta tau (cycles)"] == "+184.4†"
    assert row_60["H5.1 rank rho"] == "-0.464"
    assert r"^{\dagger}" in latex
    assert "diagnostic rather than as an accepted robustness estimate" in latex


def test_generate_one_table_writes_csv_and_latex(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A selected table can be generated independently."""

    import battery_degradation_publication.tables.generation as generation

    monkeypatch.setattr(generation, "GENERATED", tmp_path / "generated")
    monkeypatch.setattr(generation, "MACHINE", tmp_path / "machine")
    assert generate_tables(["preprocessing_summary"]) == 0
    assert (tmp_path / "generated/preprocessing_summary.tex").is_file()
    csv_path = tmp_path / "machine/preprocessing_summary.csv"
    assert csv_path.is_file()
    assert len(pd.read_csv(csv_path)) == 10
