"""Optional deterministic validation of a locally acquired source dataset."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

EXPECTED_COLUMNS = [
    "Cycle_Index",
    "Discharge Time (s)",
    "Charging time (s)",
    "C/D",
]
STUDY_SHA256 = "bb1ad32c2d1ed83ed93ec5b0e6cb17c22905b729a8a9a13ab028868e472faa48"


def validate_raw_dataset(path: Path) -> dict[str, Any]:
    """Validate source columns, checksum, battery reconstruction, and C/D identity.

    Parameters
    ----------
    path:
        User-supplied CSV path. The file is read but never modified.

    Returns
    -------
    dict[str, Any]
        Row count, reconstructed battery count, checksum, and maximum C/D error.

    Raises
    ------
    FileNotFoundError
        If the user has not placed the CSV at the documented path.
    ValueError
        If columns, checksum, battery count, or the derived-ratio identity differ.
    """

    if not path.is_file():
        raise FileNotFoundError(
            f"Place the public dataset at {path}. See data/README.md for acquisition details."
        )
    checksum = hashlib.sha256(path.read_bytes()).hexdigest()
    if checksum != STUDY_SHA256:
        raise ValueError(f"Unexpected dataset checksum: {checksum}")
    frame = pd.read_csv(path)
    if frame.columns.tolist() != EXPECTED_COLUMNS:
        raise ValueError(f"Expected columns {EXPECTED_COLUMNS}, found {frame.columns.tolist()}")
    resets = frame["Cycle_Index"].diff().lt(0).fillna(False)
    battery_id = resets.cumsum().astype(int) + 1
    if int(battery_id.max()) != 14:
        raise ValueError(f"Expected 14 reconstructed battery records, found {battery_id.max()}")
    ratio = frame["Charging time (s)"] / frame["Discharge Time (s)"]
    maximum_error = float(np.max(np.abs(frame["C/D"] - ratio)))
    if maximum_error > 1e-12:
        raise ValueError(f"C/D identity error exceeds tolerance: {maximum_error}")
    return {
        "rows": len(frame),
        "battery_records": int(battery_id.max()),
        "sha256": checksum,
        "maximum_cd_identity_error": maximum_error,
    }
