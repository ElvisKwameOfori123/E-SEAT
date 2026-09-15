# Source-data mirrors

This directory contains text mirrors of smaller E-SEAT source inputs so their contents can be inspected directly in GitHub.

Currently committed:

- `CornQP.csv`: national corn production and corn-use-for-ethanol series;
- `CornPC.csv`: county corn indicator used in descriptive exposure construction;
- `EthanolPlantsatCounties.csv`: county ethanol-plant counts;
- `ext_margin.csv`: county extensive-margin indicator.

The Ohio 2022 county table used during data preparation is stored under `../prepared/`.

The authoritative Stata analysis uses the documented source variables and preserves source suppression as missing. Exact file sizes and SHA-256 hashes are recorded in `../MANIFEST.csv`.

For the public release, original binary inputs should only be redistributed where source terms permit. Otherwise, the repository will retain acquisition instructions and hashes so locally obtained copies can be verified.
