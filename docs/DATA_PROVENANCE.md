# Data provenance

The release follows this path:

```text
public source dataset
-> deterministic battery reconstruction and cycle classification
-> accepted analytical run
-> frozen plotting artifact
-> manuscript figure
```

The source table contains cycle-level summaries. Battery identity was inferred
before duplicate analysis by incrementing `Battery_ID` whenever `Cycle_Index`
decreased, yielding 14 sequential records. The accepted preprocessing preserved
source order and all observations, classified candidate long-duration and
candidate incomplete cycles from source phase durations, and retained both
per-battery and cycle-aggregate representations.

The public release does not recompute those accepted classifications during
figure generation. It distributes the exact accepted regular-eligible rows,
aggregate summaries, transition-definition tables, H5.1 scientific summaries,
posterior-predictive plotting summaries, and M8 sensitivity summaries needed by
the ten figures.

Accepted run lineage:

- M4 aggregate smooth model: `m4_bayesian_smooth`;
- M4 definition comparison: `m4_changepoint_definitions`;
- H5.1 hierarchical model: `m5_h5_1_full_metric_final`;
- posterior predictive diagnostics: `m5_h5_1_full_metric_final/ppc`;
- sparse-data sensitivity: `m8_extended_sensitivity_01`.

`release_manifest.csv` records the full-repository source path, release path,
SHA-256 checksum, accepted run, and inclusion reason for each copied analytical
artifact, configuration file, and accepted reference figure.
