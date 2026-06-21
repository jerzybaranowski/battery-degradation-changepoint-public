# Reproducibility

The supported reference environment is Python 3.11 on macOS or Linux. The
release was built with NumPy 2.4.6, pandas 2.3.3, Matplotlib 3.11.0, PyYAML
6.0.3, Pillow 12.2.0, pypdf 6.13.3, and pytest 9.1.1. These versions reproduce
the figures; they are not claims about the original model-sampling environment.

The workflow is deterministic. No plotting jitter, subsampling, bootstrapping,
or model sampling occurs, so no runtime random seed is required. The M8 frozen
artifacts preserve the seeds used by the accepted analytical runs.

From the repository root:

```bash
python scripts/generate_all_figures.py
python scripts/generate_figure.py --figure fig_results_h5_ppc
python scripts/generate_all_tables.py
python scripts/generate_table.py --table hierarchical_population_results
python -m pytest
python scripts/validate_release.py
```

Figure outputs are written to `figures/generated/`. Table outputs are written to
`tables/generated/` and `tables/machine_readable/`. Typical total runtime is
below one minute on a laptop. PDF files retain vector text and axes; dense
observation layers are selectively rasterized where inherited from the accepted
plotting implementation.

Validation checks:

- every configured PDF and PNG exists and is non-empty;
- PDF page size and PNG pixel dimensions match the configured physical size and
  300-DPI export;
- every frozen artifact checksum matches `release_manifest.csv`;
- all eight active table identifiers are represented;
- generated table LaTeX is byte-identical to the active manuscript source;
- table CSV files are non-empty and preserve manuscript labels and rounding;
- dagger marks, diagnostic notes, MDPI full-width formatting, and bibliography
  references are validated;
- no NetCDF, symbolic link, prohibited internal file, oversized file, or known
  machine-specific path is included.

Exact PDF hashes are not compared because PDF metadata and font subset names may
vary. Numerical input checksums and structural output checks are authoritative.
