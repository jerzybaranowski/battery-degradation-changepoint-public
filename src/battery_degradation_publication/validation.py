"""Structural, checksum, size, and output validation for the public release."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path
from typing import Any

import yaml
from PIL import Image
from pypdf import PdfReader

from .figure_config import PACKAGE_ROOT, load_config

PROHIBITED_NAMES = {
    "AGENTS.md",
    "PLANS.md",
    ".agent",
    ".agents",
    "skills",
    "hooks",
    ".ipynb_checkpoints",
    "__pycache__",
    ".pytest_cache",
}
IGNORED_ROOT_NAMES = {".git"}
ACTIVE_TABLES = {
    "battery_technology_context",
    "degradation_mechanisms_observability",
    "preprocessing_summary",
    "transition_definitions",
    "computation_gates",
    "changepoint_results",
    "hierarchical_population_results",
    "truncation_results",
}


def sha256_file(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of one file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_release(root: Path = PACKAGE_ROOT) -> dict[str, Any]:
    """Validate release contents and generated manuscript figures.

    The checks are deterministic and do not alter package files.
    """

    errors: list[str] = []
    warnings: list[str] = []
    table_status: dict[str, str] = {}
    config = load_config(root / "configs/figure-config.yaml")
    manifest_path = root / "release_manifest.csv"
    if not manifest_path.is_file():
        errors.append("release_manifest.csv is missing")
        manifest_rows: list[dict[str, str]] = []
    else:
        with manifest_path.open(newline="", encoding="utf-8") as handle:
            manifest_rows = list(csv.DictReader(handle))
        manifest_by_path = {row["package_path"]: row for row in manifest_rows}
        for identifier in ACTIVE_TABLES:
            required_manifest_entries = {
                f"tables/reference/{identifier}.tex",
                f"tables/generated/{identifier}.tex",
                f"tables/machine_readable/{identifier}.csv",
            }
            missing_entries = required_manifest_entries - manifest_by_path.keys()
            if missing_entries:
                errors.append(
                    f"Table manifest entries missing for {identifier}: {sorted(missing_entries)}"
                )

    for row in manifest_rows:
        package_path = root / row["package_path"]
        if not package_path.is_file():
            errors.append(f"Manifest file is missing: {row['package_path']}")
            continue
        actual = sha256_file(package_path)
        if actual != row["sha256"]:
            errors.append(f"Checksum mismatch: {row['package_path']}")

    release_paths = [
        path
        for path in root.rglob("*")
        if path.relative_to(root).parts[0] not in IGNORED_ROOT_NAMES
    ]

    for path in release_paths:
        if path.name in PROHIBITED_NAMES:
            errors.append(f"Prohibited internal path included: {path.relative_to(root)}")
        if path.is_symlink():
            errors.append(f"Symbolic link included: {path.relative_to(root)}")
        if path.is_file() and path.suffix.lower() in {".nc", ".nc4"}:
            errors.append(f"Posterior archive included: {path.relative_to(root)}")
        if path.is_file() and path.stat().st_size > 25 * 1024 * 1024:
            errors.append(f"File exceeds 25 MB: {path.relative_to(root)}")

    # Build the platform-specific markers from components so the validator does
    # not mistake its own detection patterns for leaked local paths.
    forbidden_fragments = (
        "/" + "Users" + "/",
        "\\" + "Users" + "\\",
        "jerzy" + "baranowski" + "/" + "GitHub",
    )
    for path in release_paths:
        if not path.is_file() or path.suffix.lower() in {".pdf", ".png"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for fragment in forbidden_fragments:
            if fragment in text:
                errors.append(f"Absolute or machine-specific path in {path.relative_to(root)}")

    for figure_id, entry in config["figures"].items():
        expected_width = float(entry["width_in"])
        expected_height = float(entry["height_in"])
        expected_pixels = (
            round(expected_width * int(config["rendering"]["png_dpi"])),
            round(expected_height * int(config["rendering"]["png_dpi"])),
        )
        pdf_path = root / "figures/generated" / f"{figure_id}.pdf"
        png_path = root / "figures/generated" / f"{figure_id}.png"
        for path in (pdf_path, png_path):
            if not path.is_file() or path.stat().st_size == 0:
                errors.append(f"Generated output is missing or empty: {path.relative_to(root)}")
        if pdf_path.is_file():
            page = PdfReader(pdf_path).pages[0]
            size = (float(page.mediabox.width) / 72, float(page.mediabox.height) / 72)
            if abs(size[0] - expected_width) > 0.01 or abs(size[1] - expected_height) > 0.01:
                errors.append(f"PDF dimensions differ for {figure_id}: {size}")
        if png_path.is_file():
            with Image.open(png_path) as image:
                if image.size != expected_pixels:
                    errors.append(
                        f"PNG dimensions differ for {figure_id}: {image.size} != {expected_pixels}"
                    )

    table_manifest_path = root / "table_manifest.yaml"
    if not table_manifest_path.is_file():
        errors.append("table_manifest.yaml is missing")
    else:
        table_manifest = yaml.safe_load(table_manifest_path.read_text(encoding="utf-8"))
        entries = table_manifest.get("tables", []) if isinstance(table_manifest, dict) else []
        represented = {entry.get("table_id") for entry in entries if isinstance(entry, dict)}
        if represented != ACTIVE_TABLES:
            errors.append(
                "Active table manifest mismatch: "
                f"missing={sorted(ACTIVE_TABLES - represented)}, "
                f"unexpected={sorted(represented - ACTIVE_TABLES)}"
            )
        bibliography = root / "tables/reference/references.bib"
        bibliography_keys: set[str] = set()
        if bibliography.is_file():
            bibliography_keys = set(
                re.findall(r"^@\w+\{\s*([^,\s]+)", bibliography.read_text(encoding="utf-8"), re.M)
            )
        else:
            errors.append("Curated-table bibliography is missing")

        forbidden_latex = re.compile(r"\\(?:footnotesize|scriptsize|resizebox)\b")
        for identifier in sorted(ACTIVE_TABLES):
            generated_tex = root / "tables/generated" / f"{identifier}.tex"
            reference_tex = root / "tables/reference" / f"{identifier}.tex"
            machine_csv = root / "tables/machine_readable" / f"{identifier}.csv"
            local_errors: list[str] = []
            for path in (generated_tex, reference_tex, machine_csv):
                if not path.is_file() or path.stat().st_size == 0:
                    local_errors.append(f"missing or empty {path.relative_to(root)}")
            if generated_tex.is_file() and reference_tex.is_file():
                generated_text = generated_tex.read_text(encoding="utf-8")
                reference_text = reference_tex.read_text(encoding="utf-8")
                if generated_text != reference_text:
                    local_errors.append("generated LaTeX differs from active manuscript source")
                if forbidden_latex.search(generated_text):
                    local_errors.append("prohibited LaTeX size or resize command present")
                cited: set[str] = set()
                for group in re.findall(r"\\cite\{([^}]+)\}", generated_text):
                    cited.update(key.strip() for key in group.split(","))
                missing_keys = cited - bibliography_keys
                if missing_keys:
                    local_errors.append(f"bibliography keys missing: {sorted(missing_keys)}")
            if identifier == "truncation_results" and generated_tex.is_file():
                text = generated_tex.read_text(encoding="utf-8")
                if r"^{\dagger}" not in text or "diagnostic" not in text:
                    local_errors.append("dagger or diagnostic-only note is missing")
                if r"\begin{adjustwidth}{-\extralength}{0cm}" not in text:
                    local_errors.append("MDPI full-width formatting is missing")
            table_status[identifier] = "passed" if not local_errors else "failed"
            errors.extend(f"{identifier}: {message}" for message in local_errors)

    if not (root / "data/raw/data_new.csv").exists():
        warnings.append("Raw source dataset is not redistributed; frozen plotting data are used.")

    return {
        "status": "passed" if not errors else "failed",
        "figure_count": len(config["figures"]),
        "table_count": len(ACTIVE_TABLES),
        "tables": table_status,
        "errors": errors,
        "warnings": warnings,
    }
