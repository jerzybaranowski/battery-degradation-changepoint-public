# Manuscript figure replication package

Paper title: *Hierarchical Bayesian Changepoint Analysis of Lithium-Ion
Battery Degradation under Incomplete Cycle Observations*

This repository reproduces ten manuscript figures and all eight active
manuscript tables for the retrospective, uncertainty-aware changepoint analysis
of cycle-level battery-health indicators. It uses frozen accepted analytical
summaries and plotting tables. It does not rerun the complete Bayesian analysis
by default.

## Scope

The package reproduces all files named `fig_results_*.pdf` and
`fig_results_*.png` under `figures/generated/`. It regenerates five computed
manuscript tables from frozen analytical artifacts and preserves the exact
LaTeX plus transparent CSV representation of three author-curated contextual or
methodological tables. Numerical table regeneration is distinct from inclusion
of literature-informed author synthesis.

The aggregate model uses cycle-level median observations, while the
hierarchical model uses per-battery observations; these observation units are
not interchangeable. The figures and tables describe retrospective transition
analysis, not prospective remaining-useful-life prediction.

The package does not include posterior NetCDF archives, PyMC/ArviZ, model
development history, failed runs, internal plans, notebooks, manuscript drafts,
or agent configuration. Full statistical re-estimation remains in the authors'
complete research repository.

## Structure

- `data/frozen_results/`: accepted compact plotting inputs;
- `src/battery_degradation_publication/`: loaders, builders, rendering, validation;
- `configs/`: palette, typography, dimensions, and export profiles;
- `figures/reference/`: accepted comparison artifacts;
- `figures/generated/`: outputs created by this release;
- `tables/reference/`: accepted active manuscript table sources;
- `tables/generated/`: regenerated manuscript-ready LaTeX;
- `tables/machine_readable/`: CSV representations of all active tables;
- `docs/`: provenance, scope, figure manifest, and validation records.

## Installation

Python 3.11 is the supported reproduction version.

```bash
conda env create -f environment.yml
conda activate battery-degradation-publication
```

Alternatively:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Dataset

Raw-data redistribution permission is unresolved, so the source CSV is not
included. See `data/README.md` for the expected filename, columns, checksum,
and acquisition placeholders. The default figure workflow is self-contained
because it uses frozen accepted plotting data.

## Generate figures

```bash
python scripts/generate_all_figures.py
```

Generate one figure:

```bash
python scripts/generate_figure.py --figure fig_results_h5_ppc
```

Equivalent Make target:

```bash
make figures
```

Generate all active tables:

```bash
python scripts/generate_all_tables.py
```

Generate one table:

```bash
python scripts/generate_table.py --table hierarchical_population_results
```

Generate and validate the complete manuscript asset set:

```bash
make publication-assets
```

Expected runtime is under one minute on a typical laptop and requires less than
1 GB of memory. No random sampling is performed.

## Validate

```bash
python -m pytest
python scripts/validate_release.py
```

Validation checks frozen-artifact checksums, required PDF/PNG outputs, physical
dimensions, PNG resolution, prohibited files, NetCDF exclusion, file-size
limits, symbolic links, and machine-specific paths.

## Citation, licence, and contact

Complete the remaining placeholders in `CITATION.cff` after the article DOI,
repository URL, archive DOI, and release version are known. Correspondence:
Jerzy Baranowski, `jb@agh.edu.pl`.

No applicable software licence was present in the source repository. See
`LICENSE_PENDING.md`; a licence must be selected before public release.
