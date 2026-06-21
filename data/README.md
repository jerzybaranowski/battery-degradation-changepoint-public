# Dataset acquisition

The raw cycle-level dataset is not redistributed in this package because the
source repository does not document a dataset licence or terms that clearly
permit redistribution.

- Exact dataset title: `Battery Remaining Useful Life (RUL)`
- Public source URL:
  `https://www.kaggle.com/datasets/ignaciovinuales/battery-remaining-useful-life-rul`
- Curator named by the manuscript: I. Viñuales
- Manuscript access date: 21 June 2026
- Expected local filename: `data_new.csv`
- Place it at: `data/raw/data_new.csv`
- Study-file SHA-256:
  `bb1ad32c2d1ed83ed93ec5b0e6cb17c22905b729a8a9a13ab028868e472faa48`
- Expected columns: `Cycle_Index`, `Discharge Time (s)`,
  `Charging time (s)`, and `C/D`

After acquiring the dataset under its applicable terms, run:

```bash
cp /path/to/data_new.csv data/raw/data_new.csv
python scripts/prepare_data.py
```

The figure workflow does not require the raw CSV. It uses frozen accepted
plotting artifacts in `data/frozen_results/`. The optional preparation command
validates the checksum, reconstructs 14 battery records from cycle-index resets,
and verifies the documented `C/D` identity without writing transformed data.
