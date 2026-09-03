# E-SEAT

## Ethanol Spatial Exposure and Agricultural Transition framework

E-SEAT is a reproducible county-level empirical framework for estimating heterogeneous agricultural responses to U.S. corn-ethanol demand and examining the persistence of corn specialization across the U.S. Corn Belt, 1997–2022.

## Study coverage

The empirical panel covers 1,048 counties in Illinois, Indiana, Iowa, Kansas, Michigan, Minnesota, Missouri, Nebraska, North Dakota, Ohio, South Dakota, and Wisconsin across six Census of Agriculture waves: 1997, 2002, 2007, 2012, 2017, and 2022.

The corrected Revision 1 backcast contains 990 eligible counties.

## E-SEAT workflow

E-SEAT links the data and analytical steps in one reproducible sequence:

1. assemble the county panel and restore source missingness;
2. apply the documented Ohio 2022 corn-acreage and government-payment correction;
3. construct county corn share, crop intensity, economic outcomes, and predetermined 1997 exposure conditions;
4. construct the national corn-ethanol demand trajectory;
5. estimate county and Census-year fixed-effects specifications;
6. estimate event-style differential dynamics;
7. translate the estimated differential responses into ethanol-demand scenarios;
8. construct the 2022 backcast and threshold classifications;
9. run benchmark, reversibility, specification, inference, and sample-sensitivity checks;
10. export frozen county-level analytical outputs; and
11. render publication maps from the frozen Stata outputs using the 2023 U.S. Census Cartographic Boundary county geometry.

## Analytical implementation

**Stata is the authoritative analytical pipeline.** It performs data construction, quality assurance, estimation, scenario translation, backcasting, classification, table generation, and county-level output generation.

**Python is used for publication cartography.** It reads frozen county-level Stata outputs and joins them to the Census cartographic boundary geometry by county FIPS/GEOID.

## Software

The final Revision 1 analysis uses StataNow 18.5 with the following user-written packages:

- `ftools`
- `reghdfe`
- `estout`
- `spmap`
- `coefplot`
- `shp2dta`

The publication cartography uses Python with:

- `numpy`
- `pandas`
- `geopandas`
- `matplotlib`
- `shapely`
- `pyogrio`

Exact Python package versions will be frozen with the public replication release.

## Core project inputs

The final Revision 1 master pipeline expects the following analytical inputs:

- `AgDBase.dta`
- `CensusofAgData.dta`
- `ohio_2022_corn_govpayment_corrections.dta`
- `EthanolPlantsatCounties.dta`
- `CornQP.dta`
- `ext_margin.dta`
- `CornPC.dta`
- `cb_2023_midwest_counties_500k.zip`

Data files are being added only after provenance and redistribution checks are completed. See [`data/README.md`](data/README.md) and [`spatial/README.md`](spatial/README.md).

## Frozen Revision 1 integrity checks

The final pipeline verifies the following checkpoints:

- panel spine: 1,048 counties × 6 waves = 6,288 county-year rows;
- Ohio 2022 observed county corn-acreage sum: 3,313,863 acres;
- Ohio 2022 suppressed corn-acreage counties: 2;
- Ohio 2022 county government-payment sum: $136,764,000;
- Census cartographic boundary counties: 1,055;
- analytical counties matched to the map: 1,048;
- corrected backcast-eligible counties: 990; and
- final backcast classes: 439 / 14 / 17 / 37 / 483.

A replication run should stop for inspection if a hard integrity check fails.

## Repository structure

```text
E-SEAT/
├── code/
│   ├── stata/
│   └── python/
├── data/
├── spatial/
├── outputs/
├── qa/
└── documentation/
```

## Manuscript

The framework accompanies the *Ecological Economics* manuscript **“Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt”** (ECOLEC-D-26-03083).

## Author

Elvis Kwame Ofori  
Plant and AgriBiosciences Research Centre (PABC), Ryan Institute  
University of Galway, Ireland

## License

Repository code is released under the MIT License. Source datasets and spatial files retain the terms of their original providers.
