# Data

This directory documents the analytical inputs used by the final E-SEAT Revision 1 pipeline.

## Core analytical inputs

| File | Role in the final pipeline |
| --- | --- |
| `AgDBase.dta` | Master county panel and analytical data spine. |
| `CensusofAgData.dta` | Source Census of Agriculture fields used to restore raw missingness for harvested corn acreage and government payments. |
| `ohio_2022_corn_govpayment_corrections.dta` | Documented Ohio 2022 correction based on official USDA Census county tables. |
| `EthanolPlantsatCounties.dta` | County ethanol-plant information used in descriptive and robustness analyses. |
| `CornQP.dta` | National corn production and use series used to construct the ethanol-demand trajectory. |
| `ext_margin.dta` | County extensive-margin indicator used in descriptive exposure construction. |
| `CornPC.dta` | County corn input used in the descriptive exposure workflow. |

## Data handling

The final pipeline restores source missingness before constructing analytical variables. Harvested corn acreage and government-payment values that are suppressed or unavailable remain missing rather than being converted to zero.

The Ohio 2022 correction restores 86 observed county corn-acreage values, retains Belmont and Cuyahoga as suppressed for corn acreage, and restores all 88 reported county government-payment totals.

## Repository release plan

Each data file will be placed in one of three groups before the repository is made public:

- **redistributable source data**, committed with provider attribution;
- **derived or correction data**, committed with provenance documentation; or
- **source-retrieval data**, documented with an official download source and preparation instructions.

No analytical input will be substituted with an older or ancillary file solely to make the repository appear complete.
