# E-SEAT data

This directory documents the inputs and preparation sequence used by the frozen Revision 1 E-SEAT workflow for *Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt*.

## Academic source acknowledgement

Part of the source material used in assembling the E-SEAT database was drawn from the publicly available `Papers/EthanolCorn` research repository accompanying:

> **Le, H. and Gálvez-Soriano, O.** *Biofuel Growth: The Unintended Effects of the Ethanol Boom on Farmland Values*. **Applied Economic Perspectives and Policy**. https://doi.org/10.1002/aepp.70071

Those materials were combined with additional official and independently assembled inputs used by E-SEAT. They are therefore acknowledged as an upstream academic data and estimation source rather than presented as original E-SEAT data. Oscar Gálvez-Soriano gave explicit permission by email for use of the publicly available repository materials in this academic study.

## Preparation principle

E-SEAT treats source assembly and missing-value handling as part of normal data preparation. The workflow does not treat suppressed or unavailable Census observations as zeros. Instead it preserves the source missing-value structure, incorporates values from the relevant official county tables where needed for the assembled analytical file, and constructs the outcomes only after those source fields have been aligned.

## Preparation sequence

1. Load the 1,048-county agricultural data spine and retain the six Census waves.
2. Standardise county FIPS and verify unique county-year records.
3. Reattach the source Census fields for harvested corn acreage and government payments so source suppression remains visible.
4. Incorporate the 2022 Ohio county values assembled from the official USDA Census of Agriculture county tables.
5. Construct corn specialization as harvested corn acreage divided by total agricultural land, and rebuild the government-payment-per-acre measure from the prepared source values.
6. Merge the national corn-ethanol trajectory and predetermined county conditions.
7. Join frozen county outputs to Census cartographic geometry only after the statistical analysis is complete.

## Inputs

| File | Role |
| --- | --- |
| `AgDBase.dta` | County agricultural panel and 1,048-county analytical data spine |
| `CensusofAgData.dta` | Census source fields used to preserve original suppression/missingness |
| `prepared/ohio_2022_corn_govpayment_prepared.csv` | 2022 Ohio county corn and government-payment values assembled from official USDA county tables |
| `EthanolPlantsatCounties.dta` | County ethanol-plant information used descriptively and in robustness checks |
| `CornQP.dta` | National corn production and corn-used-for-ethanol series |
| `CornPC.dta` | County corn indicator used in descriptive exposure construction |
| `ext_margin.dta` | Extensive-margin indicator used in descriptive exposure construction |
| `cb_2023_midwest_counties_500k.zip` | 2023 Census Cartographic Boundary geometry for the twelve study states |

Text mirrors of smaller inputs are stored under `data/source/`.

## Ohio 2022 source preparation

The Ohio 2022 preparation table is drawn from the official USDA Census of Agriculture county tables used for the final analysis. It contains harvested corn acreage and government-payment values in the units expected by the analytical workflow.

Reproducibility checks confirm:

- harvested corn acreage is observed for 86 counties and sums to **3,313,863 acres**;
- Belmont (39013) and Cuyahoga (39035) are source-suppressed for harvested corn and remain missing;
- government-payment values are available for all 88 Ohio counties;
- summed county government payments equal **$136,764,000**.

These checks document source coverage and unit consistency. They do not alter the treatment of suppressed values.

## Spatial geometry

Publication maps use the official 2023 U.S. Census Cartographic Boundary county file at 1:500,000 scale, restricted to the twelve study states. The geometry contains 1,055 counties, of which 1,048 match the analytical data spine by FIPS. Spatial processing changes display geometry only and never changes county analytical values.

## File integrity

`MANIFEST.csv` records the expected byte size and SHA-256 digest of the frozen input files or public text equivalents used by the replication workflow.

## Redistribution

Source datasets remain subject to the terms of their original providers. The public repository therefore distinguishes source-data documentation from derived and prepared files. Where original binary data are not redistributed, the release should provide acquisition instructions and integrity hashes sufficient to verify a locally supplied copy.
