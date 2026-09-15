# E-SEAT

## Ethanol Spatial Exposure and Agricultural Transition

**E-SEAT** is the reproducible empirical framework supporting the study:

> **Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt**

The framework links county agricultural data, predetermined county characteristics, the national corn-ethanol demand trajectory, fixed-effects estimation, dynamic analysis, scenario translation, backcasting, persistence diagnostics, robustness checks, and publication-ready spatial outputs.

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

The panel is not treated as balanced after source suppression and missing-value restoration. Analytical samples vary by outcome.

## Analytical sequence

```text
County agricultural data
        +
National corn-ethanol demand trajectory
        +
Predetermined county conditions
        ↓
Data reconstruction and quality assurance
        ↓
County and Census-year fixed-effects estimation
        ↓
Dynamic/event-style analysis
        ↓
County-specific differential sensitivity
        ↓
Ethanol-demand scenarios
        ↓
Backcast of the estimated differential component
        ↓
Reference-point and residual-gap diagnostics
        ↓
Robustness, spatial outputs, and frozen reporting files
```

E-SEAT refers to this complete reproducible architecture rather than to a single regression equation.

## Empirical design

The primary outcome is **county corn specialization**, measured as harvested corn acreage as a percentage of total agricultural land. Crop intensity and secondary economic outcomes are also estimated.

The main fixed-effects specification interacts the national corn-ethanol demand trajectory with two predetermined county gradients:

- **1997 corn specialization**, representing starting production structure; and
- **time-invariant NCCPI**, representing soil productivity.

County fixed effects absorb persistent county characteristics. Census-year fixed effects absorb shocks common to all counties within each wave, including the level of national ethanol demand. The model therefore identifies **differential county responses**, not the aggregate national effect of ethanol demand.

## Backcast and persistence

The backcast starts from observed 2022 county corn shares and removes the estimated county-specific **differential ethanol-demand component**. The common national response absorbed by year effects remains outside the backcast.

The principal diagnostic reference point is **20% corn share**, slightly below the 2022 median of approximately 23.4%. Sensitivity is evaluated at **15%, 25%, and 30%**.

At the 20% reference point:

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

The frozen revision workflow includes:

- dynamic/event-style differential-response analysis;
- exclusion of the upper tail of baseline corn specialization;
- exclusion of the highest NCCPI counties;
- current ethanol-plant count and plant-presence specifications;
- county-clustered and state-clustered inference;
- leave-one-state-out estimation;
- alternative corn-share reference points; and
- asymmetric reversibility cases at 100%, 75%, 50%, and 25%.

State-clustered inference is reported as a sensitivity check because only twelve state clusters are available.

## Data architecture

The authoritative R1 pipeline uses the following source or reconstruction inputs:

| File | Role |
| --- | --- |
| `AgDBase.dta` | County agricultural panel and analytical data spine |
| `CensusofAgData.dta` | Census fields used to restore source missingness |
| `ohio_2022_corn_govpayment_corrections.dta` | Ohio 2022 corn-acreage and government-payment correction |
| `EthanolPlantsatCounties.dta` | County ethanol-plant information |
| `CornQP.dta` | National corn production and ethanol-use series |
| `CornPC.dta` | County corn input used in descriptive exposure construction |
| `ext_margin.dta` | Extensive-margin indicator |
| `cb_2023_midwest_counties_500k.zip` | 2023 Census Cartographic Boundary county geometry |

Source datasets remain subject to the terms and attribution requirements of their original providers. Public release should therefore prioritize reproducible acquisition instructions, derived analytical outputs, and code rather than redistributing source files where redistribution is uncertain.

## Quality assurance

Key frozen checks include:

| QA checkpoint | Expected value |
| --- | ---: |
| Analytical data spine | 6,288 potential county-year rows |
| Ohio 2022 observed county corn acreage | 3,313,863 acres |
| Ohio 2022 suppressed corn-acreage counties | 2 |
| Census cartographic counties | 1,055 |
| Spatially matched analytical counties | 1,048 |
| Backcast-eligible counties | 990 |
| Backcast classes | 439 / 14 / 17 / 37 / 483 |

The authoritative Stata workflow stops for inspection when a hard integrity check fails.

## Software and implementation

**StataNow 18.5** is the authoritative analytical environment. The main workflow uses `ftools`, `reghdfe`, `estout`, `spmap`, `coefplot`, and `shp2dta`.

Python is used only to render publication maps from frozen county-level Stata outputs. The cartographic workflow does not re-estimate analytical quantities.

The final public release is intended to contain:

```text
code/stata/FINAL_ECOLEC_R1_MASTER.do
code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py
documentation/reproducibility.md
data/README.md
outputs/
```

See `RELEASE_CHECKLIST.md` for the remaining release items.

## Repository status

This repository remains **private during manuscript revision**. The public release will provide the analytical code, quality-assurance documentation, derived county-level outputs, and publication-figure inputs, subject to source-data redistribution conditions.

The repository should not be treated as the final public replication package until every item in `RELEASE_CHECKLIST.md` is complete.

## Citation

Please cite the framework and associated study as:

> Ofori, E. K. (2026). **E-SEAT: Ethanol Spatial Exposure and Agricultural Transition framework**. Reproducible research materials for *Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt*.

A machine-readable citation is provided in `CITATION.cff`.

## Author

**Elvis Kwame Ofori**  
Plant and AgriBiosciences Research Centre (PABC), Ryan Institute  
University of Galway, Galway, Ireland

## License

Repository code is released under the **MIT License**. Source datasets and spatial files retain the terms and attribution requirements of their original providers.
