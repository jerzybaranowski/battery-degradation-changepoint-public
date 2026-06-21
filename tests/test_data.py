"""Tests for frozen analytical inputs and optional raw-data handling."""

from pathlib import Path

import pytest
from battery_degradation_publication.data import load_figure_data
from battery_degradation_publication.raw_data import validate_raw_dataset


def test_frozen_inputs_preserve_battery_ids() -> None:
    """Accepted per-battery inputs must contain exactly Battery 1 through 14."""

    data = load_figure_data()
    assert data["regular_rows"]["Battery_ID"].astype(int).unique().tolist() == list(range(1, 15))


def test_missing_raw_dataset_has_actionable_error(tmp_path: Path) -> None:
    """Optional raw-data validation must explain the expected placement."""

    with pytest.raises(FileNotFoundError, match=r"data/README\.md"):
        validate_raw_dataset(tmp_path / "data_new.csv")
