# E-SEAT

Code and data for the paper **Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt** (under revision, *Ecological Economics*).

The study asks how county corn specialisation in 12 Midwest states responds when the national corn-ethanol demand signal weakens. It uses 1,048 counties across six Census of Agriculture waves (1997, 2002, 2007, 2012, 2017, 2022).

## Files

1. `code/stata/FINAL_ECOLEC_R1_MASTER.do`: master Stata script. Runs the analysis in order: data preparation, county panel, fixed-effects estimation, sensitivity, backcast, robustness checks and export of county results.
2. `code/stata/modules/01_prepare_panel.do`: builds the county panel. Suppressed Census values stay missing; they are not set to zero.
3. `code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py`: draws the paper's maps from the county results exported by Stata. It does not re-estimate anything.
4. `data/source/`: text copies of the smaller inputs (national corn and ethanol series, county corn indicators, ethanol plants, extensive-margin indicator).
5. `data/prepared/ohio_2022_corn_govpayment_prepared.csv`: 2022 Ohio county corn acreage and government payments, taken from the official USDA county tables.
6. `data/MANIFEST.csv`: file size and SHA-256 hash of every input, so you can check your local copies.
7. `data/verify_inputs.py`: checks your input files against `MANIFEST.csv`.
8. `data/README.md` and `documentation/DATA_PREPARATION.md`: where each input comes from and how it is prepared.
9. `RELEASE_CHECKLIST.md`: checks still to complete before this is a one-command replication package.

## How to run

1. Place the inputs listed in `data/MANIFEST.csv` in `data/local/` and run `python data/verify_inputs.py`.
2. Run `code/stata/FINAL_ECOLEC_R1_MASTER.do` in Stata 18.5 (StataNow) from the repository root.
3. Run `python code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py` to draw the maps.

Stata produces all estimates. Python only draws maps.

## Data

Sources: USDA Census of Agriculture, national corn and ethanol-use series, NCCPI soil productivity, county population, ethanol plant locations, and 2023 Census county boundaries. Part of the source material comes from the public [galvez-soriano/Papers/EthanolCorn](https://github.com/galvez-soriano/Papers/tree/main/EthanolCorn) repository (Le and Gálvez-Soriano), used with permission. Original datasets keep their providers' terms.

## Status

Revision 1 materials. Some analysis modules are still to be added; see `RELEASE_CHECKLIST.md`.

## Citation and licence

Ofori, E. K. (2026). E-SEAT: Ethanol Spatial Exposure and Agricultural Transition framework. See `CITATION.cff`. Acknowledgements are in `ACKNOWLEDGEMENTS.md`.

Code: MIT licence.
