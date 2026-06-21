# Package build report

Build date: 2026-06-21

## Package structure

The release contains:

- a minimal installable Python package under `src/`;
- ten explicit figure modules plus one shared accepted builder implementation;
- eight active table generators, including five computed and three curated tables;
- release-local plotting configuration and publication styles;
- 21 frozen analytical CSV/JSON artifacts;
- eight additional frozen table-source artifacts and two resolved configurations;
- 20 accepted reference figure files;
- 20 newly generated figure files;
- eight accepted reference table files, eight generated LaTeX tables, eight CSV tables,
  and the current manuscript bibliography;
- tests, provenance documentation, citation metadata, and checksum manifests.

## Files copied

Copied inputs are recorded individually in `release_manifest.csv`:

- accepted M4 aggregate, definition-comparison, and curvature tables;
- accepted H5.1 regular-eligible rows and scientific summaries;
- accepted posterior-predictive plotting summaries;
- accepted M8 random-thinning, truncation, horizon, mask, and diagnostic tables;
- publication palette, export profiles, and Matplotlib styles;
- ten accepted PDF and ten accepted PNG reference figures.
- the eight active manuscript table sources and bibliography.

## Files refactored

The accepted publication builder was copied into
`src/battery_degradation_publication/figures/_builders.py` and changed only to
use package-relative frozen artifact paths. Ten small public modules expose one
builder per manuscript figure. Rendering, configuration, optional raw-data
validation, and release validation were separated into importable modules and
thin command-line scripts.

No new scientific transformation was introduced. The only reduced artifact is
`data/frozen_results/m8/computational_diagnostics.csv`, which selects the four
already-existing fields required by Figures 7 and 8:
`model_id`, `scenario_id`, `diagnostic_status`, and
`treedepth_saturation_count`. This removes irrelevant machine-local environment
metadata without changing plotted diagnostic status.

Computed table generators use accepted preprocessing counts, resolved sampling
configuration, exact diagnostics, M4 transition summaries, H5.1 population
summaries, and M8 truncation summaries. Generated LaTeX is byte-identical to the
current active manuscript sources. Curated table generators preserve the exact
author-approved wording and expose it as CSV with explicit provenance fields.

## Frozen artifacts created

No posterior draws or intervals were recalculated. Frozen plotting tables were
copied from accepted A1, H5.1, PPC, and M8 outputs. The package contains no
NetCDF archive and does not import PyMC or ArviZ.

## Excluded categories

Excluded: inactive manuscript table files, raw CSV redistribution, posterior NetCDF, notebooks, project plans,
agent configuration, prompts, teaching material, failed-model history,
experiment-history registries, manuscript drafts, reviewer-response files,
temporary files, caches, Git metadata, and internal audit logs.

## Dataset redistribution decision

Redistribution permission was not documented clearly enough to include the raw
CSV. `data/README.md` provides the study checksum, expected filename and
columns, placement command, and placeholders for the confirmed public title and
URL. Default figure generation remains self-contained from frozen outputs.

## Environment definition

Python 3.11 with pinned figure-reproduction versions:

- NumPy 2.4.6
- pandas 2.3.3
- Matplotlib 3.11.0
- PyYAML 6.0.3
- Pillow 12.2.0
- pypdf 6.13.3
- pytest 9.1.1 for tests

`pyproject.toml`, `environment.yml`, and `requirements.txt` are mutually
consistent.

## Commands tested

```bash
python -m pytest
python scripts/generate_all_figures.py
python scripts/generate_figure.py --figure fig_results_h5_ppc
python scripts/generate_all_tables.py
python scripts/generate_table.py --table hierarchical_population_results
python scripts/validate_release.py
make publication-assets
```

The full package was also copied outside the parent repository, installed
editable in an isolated virtual environment, tested, regenerated, and validated.

## Test and figure results

- Tests: 26 passed.
- Generated PDFs: 10.
- Generated PNGs: 10.
- Generated manuscript LaTeX tables: 8.
- Generated machine-readable tables: 8.
- Table/reference LaTeX comparison: exact for all eight active tables.
- Structural release validation: passed.
- Generated/reference PNG pixel comparison: exact for all ten figures.
- Manual contact-sheet inspection: no visible clipping or missing content.

Generated identifiers:

1. `fig_results_cd_trajectories`
2. `fig_results_transition_definitions`
3. `fig_results_h5_transition_midpoints`
4. `fig_results_h5_slope_acceleration`
5. `fig_results_h5_selected_fits`
6. `fig_results_h5_ppc`
7. `fig_results_random_thinning`
8. `fig_results_truncation_sensitivity`
9. `fig_results_post_transition_horizon`
10. `fig_results_battery11_truncation`

## Size

Final package size before this report refresh was 14,616 KiB (approximately
14.3 MiB), well below 100 MB. The package contains 150 files. The largest files are:

1. `data/frozen_results/h5/regular_eligible_cycles.csv` — 3,149,891 bytes;
2. `data/frozen_results/ppc/ppc_trajectory_summary.csv` — 2,863,668 bytes;
3. generated/reference `fig_results_h5_ppc.png` — 500,893 bytes each;
4. `data/frozen_results/m4/changepoint_method_predictions.csv` — 401,900 bytes.

No individual file exceeds 25 MB.

## Licence and unresolved issues

- Software licence: pending author selection.
- Article DOI, public repository URL, Zenodo DOI, and release version: pending.
- Author target-size review and explicit final-render approval: pending.

## Readiness assessment

The package is technically ready for author review as a separate replication
repository: it is self-contained, portable, checksum-validated, below the size
limits, reproduces all ten accepted figure PNGs exactly, and reproduces all
eight active manuscript tables without sampling. It is not ready for public
release until the licence, repository/archive identifiers, and final author
approval are completed.

## Git status

Task-created files remain untracked under `publication_release/`. The
user-supplied `docs/latex paper/` manuscript is also untracked but was not
modified by this task. Nothing was staged or committed.
