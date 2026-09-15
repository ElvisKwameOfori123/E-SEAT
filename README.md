# E-SEAT

## Ethanol Spatial Exposure and Agricultural Transition

**E-SEAT** is a reproducible empirical framework for the study:

> **Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt**

The framework links county-level agricultural data, national corn-ethanol demand, predetermined county conditions, fixed-effects estimation, dynamic analysis, scenario translation, backcasting, robustness checks, and spatial diagnostics.

Its central question is simple:

> **If the ethanol-demand signal weakens, how much of current Corn Belt specialization is likely to reverse, and how much reflects the production structure already in place?**

The analysis therefore separates **responsiveness** from **starting position**. A county can respond to a weaker ethanol-demand signal and still remain highly specialized because it begins from a very different agricultural structure.

---

## Quick start

The repository follows a simple paper-replication structure: **data → Stata analysis → frozen county outputs → Python publication maps**.

1. Review the required inputs and provenance in `data/README.md` and `data/MANIFEST.csv`.
2. The Stata master controller, `code/stata/FINAL_ECOLEC_R1_MASTER.do`, records the intended analytical sequence. The data-preparation module is already included; the remaining frozen analytical modules are still being consolidated into the public repository.
3. If the frozen Stata county outputs are already available, `code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py` can be used to render the publication maps.

Stata remains authoritative for all analytical quantities. Python is only a cartographic renderer. Until modules 02–06 are added, the repository should not be described as a complete one-command replication package.

---

## Study design

E-SEAT covers counties in:

**Illinois, Indiana, Iowa, Kansas, Michigan, Minnesota, Missouri, Nebraska, North Dakota, Ohio, South Dakota, and Wisconsin**

across six Census of Agriculture waves:

**1997, 2002, 2007, 2012, 2017, and 2022**.

| Replication checkpoint | Value |
| --- | ---: |
| Counties in analytical data spine | 1,048 |
| Census waves | 6 |
| Potential county-year observations | 6,288 |
| Principal corn-share observations | 5,977 |
| Counties in principal corn-share model | 1,005 |
| Backcast-eligible counties | 990 |
| Census cartographic counties | 1,055 |
| Analytical counties matched spatially | 1,048 |

The 1,048 × 6 structure is the common data spine. Estimation samples vary by outcome because suppressed or unavailable source values are retained as missing rather than recoded to zero.

---

## Framework

```text
SOURCE DATA
USDA Census of Agriculture
+ national corn and ethanol-use series
+ county ethanol-plant information
+ NCCPI soil productivity
+ population
+ Census county geometry
        ↓
DATA PREPARATION AND QA
harmonise county identifiers and Census waves
preserve source suppression and missingness
construct analysis-ready outcomes
        ↓
COUNTY PANEL
1997–2022
        ↓
EMPIRICAL ESTIMATION
county fixed effects
+ Census-year fixed effects
+ predetermined county gradients
+ dynamic differential-response analysis
        ↓
COUNTY SENSITIVITY
estimated response to national ethanol demand
        ↓
SCENARIO TRANSLATION AND BACKCAST
remove fractions of the estimated differential
ethanol-demand component
        ↓
PERSISTENCE DIAGNOSTICS
starting position
reference-point crossing
residual specialization
        ↓
ROBUSTNESS AND FROZEN COUNTY OUTPUTS
        ↓
PUBLICATION CARTOGRAPHY
Python renders maps from frozen Stata outputs
```

E-SEAT refers to this complete empirical architecture, not to a single regression equation.

---

## Empirical design

The principal outcome is **county corn specialization**, measured as:

> harvested corn acreage / total agricultural land × 100.

The main fixed-effects specification interacts the national corn-ethanol demand trajectory with two predetermined county gradients:

- **1997 corn specialization**, representing initial production structure;
- **time-invariant NCCPI**, representing soil productivity.

County fixed effects absorb persistent county characteristics. Census-year fixed effects absorb shocks common to all counties within each wave, including the national level of ethanol demand.

The estimated interaction terms therefore identify **differential county responses** to the national ethanol-demand trajectory. They do not identify the aggregate national effect of ethanol demand.

The workflow also estimates crop intensity and secondary economic outcomes, dynamic differential responses, robustness specifications, and spatially resolved scenario diagnostics.

---

## Backcast and structural persistence

The backcast begins from observed 2022 county corn shares and removes the estimated county-specific **differential ethanol-demand component**.

It is important to distinguish this from a literal ethanol phaseout. The common national component is absorbed by Census-year fixed effects and is not identified separately in the fixed-effects model.

The principal diagnostic reference point is a **20% corn share**, slightly below the 2022 median of approximately 23.4%. Sensitivity is also evaluated at 15%, 25%, and 30%.

| Backcast class | Counties |
| --- | ---: |
| Already at or below 20% in 2022 | 439 |
| Crosses under a 25% demand decline | 14 |
| Crosses under a 50% demand decline | 17 |
| Crosses only after complete differential-component removal | 37 |
| Remains above after complete differential-component removal | 483 |
| **Total eligible** | **990** |

The persistence result is driven primarily by differences in starting specialization rather than by large differences in estimated responsiveness.

| Diagnostic | Value |
| --- | ---: |
| SD of observed 2022 corn share | 15.55 pp |
| SD of complete-removal adjustment | 1.10 pp |
| Mean complete-removal adjustment | 4.34 pp |
| Mean starting gap among counties initially above 20% | 16.11 pp |
| Mean starting gap closed | about 27% |
| Correlation between sensitivity and 2022 corn share | about 0.09 |

These are descriptive persistence diagnostics built from the estimated differential response. They are not additional causal estimands.

---

## Data preparation and provenance

Data preparation is part of the reproducible workflow.

The analytical pipeline preserves source suppression as missing, standardises county identifiers and Census waves, incorporates official county values where required for source completion, and constructs outcomes only after the source fields have been aligned.

For the 2022 Ohio preparation, harvested corn acreage is observed for 86 of 88 counties and sums to **3,313,863 acres**. Belmont and Cuyahoga are source-suppressed and remain missing. Government-payment values are available for all 88 counties.

Detailed provenance, preparation steps, redistribution notes, and integrity checks are documented in:

- `data/README.md`
- `data/MANIFEST.csv`
- `documentation/DATA_PREPARATION.md`

Small text mirrors of selected source inputs are stored under `data/source/` for inspection. The full Stata workflow expects the documented binary inputs to be supplied locally where redistribution is not appropriate.

---

## Repository structure

```text
E-SEAT/
├── README.md
├── CITATION.cff
├── LICENSE
├── RELEASE_CHECKLIST.md
│
├── code/
│   ├── stata/
│   │   ├── FINAL_ECOLEC_R1_MASTER.do
│   │   └── modules/
│   │       └── 01_prepare_panel.do
│   │
│   └── python/
│       └── FINAL_ECOLEC_R1_PUBLICATION_MAPS.py
│
├── data/
│   ├── README.md
│   ├── MANIFEST.csv
│   ├── verify_inputs.py
│   ├── prepared/
│   └── source/
│
└── documentation/
    └── DATA_PREPARATION.md
```

The final public archive will add the remaining frozen Stata analytical modules referenced by the master controller.

---

## Analytical software

**StataNow 18.5 is the authoritative analytical environment.**

Stata performs:

- data preparation and QA;
- variable construction;
- fixed-effects estimation;
- dynamic analysis;
- robustness checks;
- scenario translation;
- backcasting;
- frozen county-level output generation.

Python is used **only for publication cartography**. It reads county values already produced by Stata, joins them to Census geometry by FIPS/GEOID, and renders the final maps. It does not re-estimate the statistical models or reconstruct the backcast.

Main scripts:

```text
code/stata/FINAL_ECOLEC_R1_MASTER.do
code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py
```

---

## Reproduction status

This repository is the **Revision 1 replication archive under finalisation**.

The data-preparation module, publication-map renderer, provenance documentation, prepared Ohio table, integrity manifest, and release checks are already included. The remaining frozen Stata analytical modules still need to be added before the repository should be treated as a complete one-command public replication package.

The release status is tracked transparently in:

> `RELEASE_CHECKLIST.md`

The repository should only be presented as the final public replication archive once the remaining modules reproduce the frozen manuscript tables, figures, and headline checks exactly.

---

## Acknowledgements and source attribution

The E-SEAT database was assembled from multiple public and official sources. **Selected data and estimation materials from the public [`galvez-soriano/Papers/EthanolCorn`](https://github.com/galvez-soriano/Papers/tree/main/EthanolCorn) repository associated with Hoanh Le and Oscar Gálvez-Soriano were used as upstream source material and combined with additional USDA Census of Agriculture, national corn and ethanol-use, spatial, and county-level inputs assembled for E-SEAT.**

The associated study is:

> **Le, H. and Gálvez-Soriano, O.** *Biofuel Growth: The Unintended Effects of the Ethanol Boom on Farmland Values*. **Applied Economic Perspectives and Policy**. https://doi.org/10.1002/aepp.70071

Oscar Gálvez-Soriano also gave the author explicit permission by email to use the publicly available repository materials for this academic study. E-SEAT therefore acknowledges both the published study and its accompanying public research materials. Any transformations, data integration, variable construction, modelling choices, errors, or interpretations in E-SEAT remain the responsibility of the E-SEAT author.

Additional provenance for the assembled analytical inputs is documented in `data/README.md` and `documentation/DATA_PREPARATION.md`.

---

## Citation

> Ofori, E. K. (2026). **E-SEAT: Ethanol Spatial Exposure and Agricultural Transition framework**. Reproducible research materials for *Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt*.

A machine-readable citation is provided in `CITATION.cff`.

---

## Author

**Elvis Kwame Ofori**  
Plant and AgriBiosciences Research Centre (PABC), Ryan Institute  
University of Galway, Galway, Ireland

---

## License

Repository code is released under the **MIT License**.

Source datasets and spatial files remain subject to the terms and attribution requirements of their original providers.
