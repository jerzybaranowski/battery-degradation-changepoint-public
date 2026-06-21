# Validation report

Build date: 2026-06-21  
Lifecycle status: technically validated; public release and manuscript-title
metadata remain pending.

## Authoritative manuscript audit

The newly supplied `docs/latex paper/main.tex` and active section inputs contain
exactly eight active table references:

1. `battery_technology_context`
2. `degradation_mechanisms_observability`
3. `preprocessing_summary`
4. `transition_definitions`
5. `computation_gates`
6. `changepoint_results`
7. `hierarchical_population_results`
8. `truncation_results`

This matches the expected list. Other `.tex` files in the manuscript `tables/`
directory are inactive and were not included. No compiled manuscript PDF was
present, so current modular LaTeX source was used as the authority.

## Commands and results

Executed in the source package:

```bash
python -m pytest
python scripts/generate_all_figures.py
python scripts/generate_all_tables.py
python scripts/generate_table.py --table hierarchical_population_results
python scripts/validate_release.py
make publication-assets
```

Results:

- 26 tests passed;
- all ten PDF files and all ten PNG files were generated;
- all eight manuscript-ready LaTeX tables and all eight CSV tables were generated;
- release validation passed with zero errors;
- the expected warning is that the raw source dataset is not redistributed.

Portability was tested by copying the complete directory to
`/tmp/battery-publication-portability`, creating an isolated Python 3.11 virtual
environment, installing the copied package in editable mode without downloading
dependencies, rerunning the 26 tests, and executing `make publication-assets`.
All checks passed.

## Figure validation

- Configured physical widths: 7.0 inches for all figures.
- Configured heights: 8.5, 5.2, 5.6, 5.4, 5.8, 6.0, 6.0, 6.0, 4.2, and
  5.8 inches in manifest order.
- PNG export: 300 DPI.
- Expected panel counts: 18, 2, 1, 2, 4, 4, 4, 4, 2, and 6.
- Every output was non-empty and had the configured PDF page and PNG pixel size.
- Rasterized PNG comparison against the accepted reference PNGs found maximum
  per-channel difference 0 for all ten figures.
- Contact-sheet review found no visible clipping, missing panels, or filename
  mismatch. This review does not constitute author approval of final renders.

## Package validation

- 81 copied or generated analytical, configuration, figure, and table artifacts are recorded in
  `release_manifest.csv`.
- All recorded SHA-256 checksums passed.
- No `.nc` or `.nc4` files are included.
- No symbolic links are included.
- No file exceeds 25 MB.
- No `AGENTS.md`, `PLANS.md`, agent configuration, notebook, cache directory,
  or internal project-management file is included.
- No absolute source path or local username remains in package text or frozen
  plotting data.

## Table-level validation

| Table | Class | Result | Comparison |
|---|---|---|---|
| `battery_technology_context` | curated | pass | Exact active LaTeX; transparent CSV |
| `degradation_mechanisms_observability` | curated | pass | Exact active LaTeX; transparent CSV |
| `preprocessing_summary` | computed | pass | Regenerated counts/shares; exact active LaTeX |
| `transition_definitions` | curated | pass | Exact active LaTeX; transparent CSV |
| `computation_gates` | computed | pass | Resolved configs and exact diagnostics; exact active LaTeX |
| `changepoint_results` | computed | pass | Accepted M4 summaries; exact active LaTeX |
| `hierarchical_population_results` | computed | pass | Accepted H5.1 summaries; exact active LaTeX |
| `truncation_results` | computed | pass | Accepted M8 summaries; dagger/note retained; exact active LaTeX |

Numerical tolerance is effectively zero after manuscript formatting: generated
LaTeX is byte-identical to the active source. CSV values retain the exact
displayed rounding. No `\footnotesize`, `\scriptsize`, or `\resizebox` command
is present. The truncation table retains full-width MDPI formatting, the dagger,
negative rank correlation, and diagnostic-only note.

The curated tables contain no direct `\cite{...}` commands. The complete current
manuscript bibliography is included and bibliography-key validation passed.

## Warnings and unresolved items

1. Raw dataset redistribution permission is unclear. The raw CSV is excluded,
   and `data/README.md` contains title/URL placeholders, expected columns, and
   the study-file checksum.
2. No applicable software licence was found. `LICENSE_PENDING.md` must be
   replaced before publication.
3. Public repository URL, article DOI, archived release DOI, and release
   version remain placeholders.
4. The authors have not yet approved the package as released or approved these
   copied renders as final manuscript artifacts.
