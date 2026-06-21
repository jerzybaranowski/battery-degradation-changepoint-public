"""Load and validate frozen analytical inputs used by the manuscript figures.

The loader exposes accepted, machine-readable plotting artifacts only. It does not
fit models, sample posteriors, recalculate uncertainty intervals, or alter the
scientific quantities stored in the release.
"""

from __future__ import annotations

from typing import Any

from .figures._builders import load_publication_figure_data


def load_figure_data() -> dict[str, Any]:
    """Return all frozen figure inputs after schema and battery-label validation.

    Returns
    -------
    dict[str, Any]
        Data frames and JSON mappings in their frozen artifact order.

    Raises
    ------
    FileNotFoundError
        If a required release artifact is absent.
    ValueError
        If a required column or the expected Battery 1--14 sequence is absent.
    """

    return load_publication_figure_data()
