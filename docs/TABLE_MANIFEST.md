# Table manifest

The authoritative manuscript source under `docs/latex paper/` contains exactly
eight active `\input{tables/...}` references. This matches the requested list;
inactive table files were excluded. A compiled manuscript PDF was not present,
so validation uses the current modular LaTeX source as the authority.

All generated LaTeX files match the corresponding manuscript table source
byte-for-byte. Computed table CSV values are regenerated from frozen accepted
artifacts without sampling. Curated CSV files preserve manuscript wording and
add provenance and citation-key columns.

| Table | Class | Accepted run | Formatting and caveat |
|---|---|---|---|
| `battery_technology_context` | curated | n/a | Qualitative author synthesis; no table-local citation keys |
| `degradation_mechanisms_observability` | curated | n/a | Literature-informed many-to-many mechanism mapping; no table-local citation keys |
| `preprocessing_summary` | computed | `m4_bayesian_smooth` | Integer counts and two-decimal shares; candidate labels remain reversible |
| `transition_definitions` | curated | n/a | Author-defined methodological roles; estimands are non-equivalent |
| `computation_gates` | computed | A1 and H5.1 accepted runs | Exact all-coordinate H5.1 rank R-hat and key-parameter ESS definitions retained |
| `changepoint_results` | computed | M4 accepted runs | Locations use one decimal and slopes six; S1 remains stability-rejected |
| `hierarchical_population_results` | computed | `m5_h5_1_full_metric_final` | Cycle quantities use three decimals, slopes six |
| `truncation_results` | computed | `m8_extended_sensitivity_01` | Dagger and diagnostic-only A1 70% case retained |

Detailed captions, source artifacts, generating functions, output paths,
rounding rules, and validation states are recorded in `table_manifest.yaml`.

## Curated-table provenance

The three curated tables contain author-approved literature synthesis or
methodological definitions. Their active table source contains no direct
`\cite{...}` command, so there are no table-local keys to validate. The full
current manuscript bibliography is included at
`tables/reference/references.bib`.

## Output convention

```text
tables/reference/<table_id>.tex
tables/generated/<table_id>.tex
tables/machine_readable/<table_id>.csv
```

Generate all tables:

```bash
python scripts/generate_all_tables.py
```

Generate one:

```bash
python scripts/generate_table.py --table hierarchical_population_results
```
