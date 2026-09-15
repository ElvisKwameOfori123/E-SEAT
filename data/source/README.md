# Source-data mirrors

This directory contains text mirrors of smaller E-SEAT inputs so that their contents can be inspected directly in GitHub.

Currently committed:

- `CornQP.csv`: national corn production and corn-use-for-ethanol series;
- `CornPC.csv`: county corn indicator used in descriptive exposure construction;
- `EthanolPlantsatCounties.csv`: county ethanol-plant counts;
- `ext_margin.csv`: county extensive-margin indicator.

The authoritative Revision 1 Stata run used the corresponding `.dta` files. Their exact byte sizes and SHA-256 hashes, together with the larger `AgDBase.dta`, `CensusofAgData.dta`, and Census cartographic geometry archive, are recorded in `../MANIFEST.csv`.

The transparent Ohio 2022 repair is stored separately in `../corrections/`.

For a final public replication release, the large/original binary inputs should only be redistributed after their source terms have been checked. If they are not redistributed, acquisition/reconstruction instructions should be retained here and the manifest hashes should be used to verify locally supplied copies.
