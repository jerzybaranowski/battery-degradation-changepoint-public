"""Tests for figure registration and frozen artifact checksums."""

from battery_degradation_publication.figure_config import load_config
from battery_degradation_publication.figures import FIGURE_BUILDERS
from battery_degradation_publication.validation import validate_release


def test_registry_matches_configuration() -> None:
    """Every configured manuscript figure must have exactly one builder."""

    assert list(FIGURE_BUILDERS) == list(load_config()["figures"])


def test_release_manifest_checksums() -> None:
    """All copied artifacts must match their recorded SHA-256 digests."""

    report = validate_release()
    checksum_errors = [error for error in report["errors"] if "Checksum" in error]
    assert checksum_errors == []
