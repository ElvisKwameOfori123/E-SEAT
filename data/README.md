# E-SEAT data

This directory documents the data inputs used by the Revision 1 E-SEAT master pipeline for *Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt*.

## Authoritative inputs

| File | Role |
| --- | --- |
| `AgDBase.dta` | County agricultural panel and 1,048-county analytical data spine |
| `CensusofAgData.dta` | Raw Census fields used to restore source missingness before rebuilding outcomes |
| `ohio_2022_corn_govpayment_corrections.dta` | Ohio 2022 harvested-corn and government-payment correction |
| `EthanolPlantsatCounties.dta` | County ethanol-plant information used in descriptive analysis and robustness checks |
| `CornQP.dta` | National corn production and corn-used-for-ethanol series |
| `CornPC.dta` | County corn indicator used in descriptive exposure construction |
| `ext_margin.dta` | Extensive-margin indicator used in descriptive exposure construction |
| `cb_2023_midwest_counties_500k.zip` | 2023 Census Cartographic Boundary county geometry for the twelve study states |

The public text mirrors of the smaller inputs are stored under `data/source/`. The Ohio correction is stored under `data/corrections/`.

## Missing values and Ohio 2022 repair

Suppressed or unavailable Census values are retained as missing rather than converted to zero. The Revision 1 pipeline first restores raw missingness from `CensusofAgData.dta`, then applies the Ohio 2022 correction from official USDA Census of Agriculture county tables.

Frozen Ohio checks are:

- observed harvested-corn acreage for 86 counties: **3,313,863 acres**;
- harvested-corn acreage suppressed for **Belmont (39013)** and **Cuyahoga (39035)**;
- government-payment values available for all 88 Ohio counties;
- summed Ohio 2022 county government payments: **$136,764,000**.

## Spatial geometry

Publication maps use the official 2023 U.S. Census Cartographic Boundary county file at 1:500,000 scale, restricted to the twelve study states. The geometry contains 1,055 counties, of which 1,048 match the analytical data spine by county FIPS. The remaining seven are cartographic-only counties.

## File integrity

`MANIFEST.csv` records the exact byte size and SHA-256 digest of the frozen input files supplied for the R1 analysis.

## Redistribution

The repository distinguishes original/source data from transparent correction and derived files. Before the repository is made public, redistribution conditions for each original source should be checked. If an original binary file cannot be redistributed, the final public release will retain its manifest entry and provide source/acquisition instructions while preserving the reproducible correction and analytical code.

## Expected placement for the Stata master

The final master script expects the eight authoritative inputs above in the configured E-SEAT input directory. Do not substitute zero-filled versions of the Census variables.
