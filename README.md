# E-SEAT

## Ethanol Spatial Exposure and Agricultural Transition

**E-SEAT** is a reproducible county-level empirical framework for analysing how U.S. corn-ethanol demand interacts with pre-existing agricultural structure and soil productivity across the Corn Belt, and how those differences shape the capacity of counties to adjust when ethanol demand changes.

The framework links historical estimation to transition analysis. It first identifies heterogeneous county responses along the national ethanol-demand trajectory, then translates those estimated responses into demand scenarios and a backcast that evaluates whether the implied adjustment is sufficient to move counties toward lower corn specialization.

> **Core idea:** responsiveness to a demand change and the ability to reach a diversification benchmark are different empirical questions.

## Study coverage

E-SEAT uses a balanced panel of counties in:

**Illinois, Indiana, Iowa, Kansas, Michigan, Minnesota, Missouri, Nebraska, North Dakota, Ohio, South Dakota, and Wisconsin.**

The panel covers six Census of Agriculture waves: **1997, 2002, 2007, 2012, 2017, and 2022**.

| Replication checkpoint | Value |
| --- | ---: |
| Counties in the analytical panel | 1,048 |
| Census waves | 6 |
| County-year observations | 6,288 |
| Backcast-eligible counties | 990 |
| Census cartographic counties | 1,055 |
| Analytical counties matched spatially | 1,048 |

## How E-SEAT works

```text
County agricultural data
        +
National corn-ethanol demand trajectory
        +
Predetermined 1997 county conditions
        ↓
Panel construction and quality assurance
        ↓
County and Census-year fixed-effects estimation
        ↓
Event-style dynamics and robustness analysis
        ↓
Ethanol-demand scenarios
        ↓
County backcast
        ↓
Transition classification
        ↓
Residual corn-specialization gap
        ↓
Frozen county outputs and maps
```

E-SEAT refers to this complete reproducible workflow. The fixed-effects model, exposure measures, scenarios, backcast, and spatial outputs remain distinct components within the framework.

## Empirical design

### County outcomes

The principal land-use outcome is **corn specialization**, measured as harvested corn area relative to total agricultural land. The framework also constructs crop intensity and economic outcomes including farmland value, government payments per acre, and annual return.

### National ethanol-demand trajectory

National ethanol demand is measured as the share of U.S. corn production used for ethanol. This common national trajectory is interacted with predetermined county characteristics to estimate heterogeneous responses across space.

### Predetermined exposure conditions

The main specification uses two county characteristics measured in 1997:

- **baseline corn specialization**, representing the county's initial agricultural structure;
- **baseline NCCPI**, representing soil productivity for commodity crop production.

County fixed effects absorb time-invariant local characteristics and Census-year fixed effects absorb shocks common to all counties. Population density is included as a time-varying control, with standard errors clustered by county in the principal estimates.

## Scenarios and backcast

Estimated county sensitivities are translated into alternative ethanol-demand paths. The backcast applies the **estimated differential ethanol-demand component** to observed 2022 corn shares and evaluates how far each eligible county moves toward a diversification benchmark.

The principal benchmark is a corn share of **20% or less of agricultural land**, with sensitivity analysis at **15%, 25%, and 30%**.

For the 20% benchmark, counties are grouped as:

| Class | Transition status |
| --- | --- |
| 1 | Already at or below the benchmark |
| 2 | Reaches the benchmark under a 25% ethanol-demand decline |
| 3 | Reaches the benchmark under a 50% ethanol-demand decline |
| 4 | Reaches the benchmark only under full differential-channel removal |
| 5 | Remains above the benchmark after full differential-channel removal |

Current frozen replication counts are:

| Class | Counties |
| ---: | ---: |
| 1 | 439 |
| 2 | 14 |
| 3 | 17 |
| 4 | 37 |
| 5 | 483 |
| **Total eligible** | **990** |

For counties that remain above the benchmark, E-SEAT calculates the **residual corn-specialization gap**, the remaining percentage-point distance from the selected threshold after the estimated differential demand component has been removed.

## Robustness and sensitivity

The replication workflow includes:

- event-style differential dynamics;
- influential-observation exclusions for baseline corn specialization and NCCPI;
- ethanol-plant count and plant-presence specifications;
- county- and state-clustered inference;
- leave-one-state-out estimation;
- alternative diversification benchmarks;
- asymmetric reversibility tests; and
- state-level scenario and transition summaries.

## Data architecture

The current analytical pipeline uses:

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

The data architecture draws principally on the **USDA Census of Agriculture**, USDA national corn-use data, USDA NRCS **NCCPI**, county ethanol-plant information, population data, and official U.S. Census cartographic boundaries.

Detailed provenance and preparation notes are maintained in `data/README.md` and `spatial/README.md`.

## Quality assurance

E-SEAT embeds reproducibility checks in the analytical workflow. Key frozen checks include:

| QA checkpoint | Expected value |
| --- | ---: |
| County-year panel | 6,288 rows |
| Ohio 2022 observed county corn acreage | 3,313,863 acres |
| Ohio 2022 suppressed corn-acreage counties | 2 |
| Ohio 2022 county government payments | $136,764,000 |
| Census cartographic counties | 1,055 |
| Spatially matched analytical counties | 1,048 |
| Backcast-eligible counties | 990 |
| Transition classes | 439 / 14 / 17 / 37 / 483 |

A replication run stops for inspection when a hard integrity check fails.

## Analytical implementation

### Stata

**Stata is the authoritative analytical pipeline.** The master workflow performs data reconstruction, quality assurance, variable construction, fixed-effects estimation, event-style analysis, scenario translation, backcasting, robustness testing, table generation, and frozen county-level exports.

```text
code/stata/FINAL_ECOLEC_R1_MASTER.do
```

### Python

Python is used for publication cartography from the frozen Stata county outputs. Analytical values are joined to the 2023 Census Cartographic Boundary geometry using county FIPS/GEOID.

```text
code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py
```

## Repository structure

```text
E-SEAT/
├── README.md
├── LICENSE
├── .gitignore
├── code/
│   ├── stata/
│   └── python/
├── data/
├── spatial/
├── outputs/
│   ├── tables/
│   ├── figures/
│   ├── maps/
│   └── county_outputs/
├── qa/
└── documentation/
```

## Reproducing the analysis

Once the documented inputs are placed in the expected locations:

```text
1. Run code/stata/FINAL_ECOLEC_R1_MASTER.do
2. Verify the embedded QA checkpoints
3. Run code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py
4. Compare the generated tables, figures, county outputs, and maps with the frozen release outputs
```

## Main outputs

E-SEAT produces:

- fixed-effects regression tables;
- event-style dynamics;
- descriptive exposure diagnostics;
- ethanol-demand scenario summaries;
- backcast transition classifications;
- benchmark-sensitivity results;
- transition-group profiles;
- residual-gap summaries;
- asymmetric-reversibility results;
- frozen county-level analytical files; and
- county-level publication maps.

## Software

The analytical workflow was developed in **StataNow 18.5** using `ftools`, `reghdfe`, `estout`, `spmap`, `coefplot`, and `shp2dta`.

Publication cartography uses Python with `numpy`, `pandas`, `geopandas`, `matplotlib`, `shapely`, and `pyogrio`.

## Citation

Please cite the framework and associated study as:

> Ofori, E. K. (2026). **E-SEAT: Ethanol Spatial Exposure and Agricultural Transition framework**. Reproducible research code and data documentation for *Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt*.

A machine-readable `CITATION.cff` file will be included with the release package.

## Author

**Elvis Kwame Ofori**  
Plant and AgriBiosciences Research Centre (PABC), Ryan Institute  
University of Galway, Galway, Ireland

## License

Repository code is released under the **MIT License**. Source datasets and spatial files retain the terms and attribution requirements of their original providers.
