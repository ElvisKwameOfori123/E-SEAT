# E-SEAT

## Ethanol Spatial Exposure and Agricultural Transition

**E-SEAT** is the reproducible empirical framework supporting the study:

> **Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt**

The framework links source-data preparation, county panel construction, predetermined county conditions, the national corn-ethanol demand trajectory, fixed-effects estimation, dynamic analysis, scenario translation, backcasting, persistence diagnostics, robustness checks, and publication-ready spatial outputs.

The central empirical distinction is between **responsiveness** and **starting position**. Counties can respond to a weaker ethanol-demand signal yet remain highly specialized because they begin from very different production structures.

## Study coverage

The study covers counties in **Illinois, Indiana, Iowa, Kansas, Michigan, Minnesota, Missouri, Nebraska, North Dakota, Ohio, South Dakota, and Wisconsin** across six Census of Agriculture waves: **1997, 2002, 2007, 2012, 2017, and 2022**.

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

The 1,048 × 6 structure is the **data spine**. Estimation samples vary by outcome because suppressed or unavailable source values are retained as missing rather than recoded to zero.

## How E-SEAT works

```text
SOURCE DATA
USDA Census of Agriculture + national corn/ethanol series
+ county ethanol-plant information + NCCPI + population
+ Census cartographic geometry
        ↓
DATA PREPARATION
harmonise county FIPS and Census years
preserve source suppression/missingness
incorporate county values from the relevant official source tables
construct analysis-ready outcomes and predetermined county conditions
        ↓
COUNTY PANEL
1,048-county analytical data spine, 1997–2022
        ↓
EMPIRICAL ESTIMATION
county and Census-year fixed effects
+ dynamic/event-style differential response
        ↓
COUNTY SENSITIVITY
response to national ethanol demand along predetermined gradients
        ↓
SCENARIOS AND BACKCAST
remove fractions of the estimated differential ethanol-demand component
        ↓
PERSISTENCE DIAGNOSTICS
starting position, reference-point crossing, residual gaps
        ↓
ROBUSTNESS + FROZEN COUNTY OUTPUTS
        ↓
PYTHON PUBLICATION CARTOGRAPHY
render maps only from Stata-produced county values
```

E-SEAT refers to this complete reproducible architecture rather than to a single regression equation.

## Data preparation

Data preparation is treated as part of the empirical design, not as a separate post-estimation adjustment. The workflow begins from the assembled county panel and source Census fields, standardises county identifiers and Census waves, restores the source missing-value structure, incorporates official county values where the assembled file requires source-table completion, and then constructs the analysis-ready outcomes.

For 2022 Ohio, harvested corn acreage and government-payment fields are read directly from the official USDA Census of Agriculture county tables used in the final analytical file. Two harvested-corn observations, Belmont and Cuyahoga, are source-suppressed and therefore remain missing. Government-payment values are available for all 88 counties. These steps are ordinary source preparation and are checked through reproducibility assertions.

The main analytical corn outcome is then constructed consistently for all counties as:

> harvested corn acreage / total agricultural land × 100.

This preparation logic ensures that suppression is not interpreted as zero and that the same variable definitions feed estimation, backcasting, tables, and maps.

## Empirical design

The primary outcome is **county corn specialization**, measured as harvested corn acreage as a percentage of total agricultural land. Crop intensity and secondary economic outcomes are also estimated.

The main fixed-effects specification interacts the national corn-ethanol demand trajectory with two predetermined county gradients:

- **1997 corn specialization**, representing starting production structure; and
- **time-invariant NCCPI**, representing soil productivity.

County fixed effects absorb persistent county characteristics. Census-year fixed effects absorb shocks common to all counties within each wave, including the level of national ethanol demand. The model therefore identifies **differential county responses**, not the aggregate national effect of ethanol demand.

## Backcast and persistence

The backcast starts from observed 2022 county corn shares and removes the estimated county-specific **differential ethanol-demand component**. The common national response absorbed by year effects remains outside the backcast.

The principal diagnostic reference point is **20% corn share**, slightly below the 2022 median of approximately 23.4%. Sensitivity is evaluated at **15%, 25%, and 30%**.

| Backcast class | Counties |
| --- | ---: |
| Already at or below 20% in 2022 | 439 |
| Crosses under a 25% demand decline | 14 |
| Crosses under a 50% demand decline | 17 |
| Crosses only after complete differential-component removal | 37 |
| Remains above after complete differential-component removal | 483 |
| **Total eligible** | **990** |

The paper's central persistence result is that starting specialization varies far more than the estimated adjustment:

- SD of observed 2022 corn share: **15.55 percentage points**
- SD of complete-removal adjustment: **1.10 percentage points**
- Mean complete-removal adjustment: **4.34 percentage points**
- Mean starting gap among counties initially above 20%: **16.11 percentage points**
- Share of the mean starting gap closed: **about 27%**
- Correlation between sensitivity and 2022 corn share: **about 0.09**

These quantities are descriptive decompositions of persistence rather than additional causal estimands.

## Robustness

The frozen R1 workflow includes dynamic differential-response analysis, influential-observation exclusions, current ethanol-plant specifications, alternative clustering, leave-one-state-out estimation, alternative corn-share reference points, and asymmetric reversibility cases.

State-clustered inference is treated as a sensitivity check because only twelve state clusters are available.

## Data architecture

The public replication workflow uses:

| File | Role |
| --- | --- |
| `AgDBase.dta` | County agricultural panel and analytical data spine |
| `CensusofAgData.dta` | Census source fields used to preserve the original missing-value structure |
| `ohio_2022_corn_govpayment_prepared.csv` | 2022 Ohio county corn and government-payment values assembled from official USDA county tables |
| `EthanolPlantsatCounties.dta` | County ethanol-plant information |
| `CornQP.dta` | National corn production and ethanol-use series |
| `CornPC.dta` | County corn input used in descriptive exposure construction |
| `ext_margin.dta` | Extensive-margin indicator |
| `cb_2023_midwest_counties_500k.zip` | 2023 Census Cartographic Boundary county geometry |

See `data/README.md` for the preparation sequence and provenance.

## Quality assurance

Key frozen checks include:

| QA checkpoint | Expected value |
| --- | ---: |
| Analytical data spine | 6,288 potential county-year rows |
| Ohio 2022 observed county corn acreage | 3,313,863 acres |
| Ohio 2022 source-suppressed corn counties | 2 |
| Ohio 2022 county government payments | $136,764,000 |
| Census cartographic counties | 1,055 |
| Spatially matched analytical counties | 1,048 |
| Backcast-eligible counties | 990 |
| Backcast classes | 439 / 14 / 17 / 37 / 483 |

These are reproducibility checks on data preparation and analytical output. They are not separate estimands.

## Software and implementation

**StataNow 18.5 is the authoritative analytical environment.** Stata performs data preparation, quality assurance, variable construction, estimation, dynamic analysis, scenario translation, backcasting, robustness analysis, and the export of frozen county-level values.

Python is used **only for publication cartography**. It reads the frozen county values exported by Stata, joins them to the 2023 Census Cartographic Boundary geometry by FIPS/GEOID, and renders the journal maps. It does not estimate regressions, construct county sensitivities, or recalculate the backcast.

```text
code/stata/FINAL_ECOLEC_R1_MASTER.do
code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py
```

## Repository status

This repository remains **private during manuscript revision**. The public release should be treated as final only after the executable Stata modules, the original Python renderer, frozen outputs, provenance notes, and final reproduction checks are complete.

## Citation

> Ofori, E. K. (2026). **E-SEAT: Ethanol Spatial Exposure and Agricultural Transition framework**. Reproducible research materials for *Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt*.

A machine-readable citation is provided in `CITATION.cff`.

## Author

**Elvis Kwame Ofori**  
Plant and AgriBiosciences Research Centre (PABC), Ryan Institute  
University of Galway, Galway, Ireland

## License

Repository code is released under the **MIT License**. Source datasets and spatial files retain the terms and attribution requirements of their original providers.
