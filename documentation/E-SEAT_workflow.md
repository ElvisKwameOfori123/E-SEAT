# E-SEAT empirical workflow

## Framework name

**Ethanol Spatial Exposure and Agricultural Transition (E-SEAT) framework**

## Empirical sequence

E-SEAT reproduces the analysis through the following sequence.

### 1. County data spine

Construct the twelve-state county panel for 1997, 2002, 2007, 2012, 2017, and 2022 and verify unique county FIPS-year observations.

Expected panel spine: **1,048 counties and 6,288 county-year rows**.

### 2. Source-value restoration and Ohio 2022 correction

Restore harvested corn acreage and government payments from the source Census of Agriculture data before rebuilding analytical variables.

Apply the documented Ohio 2022 correction using the official county-table values. The frozen checks are:

- observed Ohio county corn acreage: **3,313,863 acres**;
- suppressed Ohio corn counties: **2**;
- Ohio county government payments: **$136,764,000**.

### 3. Analytical variables

Rebuild county corn specialization as harvested corn acreage divided by total agricultural land, together with crop intensity and the economic outcomes used in the empirical specifications.

Predetermined exposure conditions are measured in 1997 and carried through the panel.

### 4. National ethanol-demand trajectory

Construct the national ethanol-demand measure from the share of U.S. corn production used for ethanol.

### 5. Fixed-effects estimation

Estimate county and Census-year fixed-effects specifications interacting the national ethanol-demand trajectory with predetermined county corn specialization and soil productivity.

### 6. Event-style dynamics

Estimate differential dynamics across Census waves using the pre-boom exposure construction and the 1997 reference year.

### 7. Scenario translation

Translate estimated county differential responses into alternative ethanol-demand paths and county-level adjustment measures.

### 8. Backcast

Apply the estimated differential component to the corrected 2022 county values and compare simulated corn shares with the reference threshold used in the manuscript.

Expected backcast-eligible sample: **990 counties**.

Frozen class counts:

- Class 1: 439
- Class 2: 14
- Class 3: 17
- Class 4: 37
- Class 5: 483

### 9. Sensitivity and robustness

Run the specification, inference, sample-exclusion, plant-control, benchmark, and reversibility checks reported in the revision materials.

### 10. Frozen county outputs

Export the county-level values used for tables, classification summaries, residual-gap analysis, and cartography.

### 11. Publication cartography

Render final county maps using the 2023 Census Cartographic Boundary county geometry at 1:500,000 scale. Join analytical outputs to geometry by FIPS/GEOID.

Expected geometry checks:

- 1,055 geometry counties;
- 1,048 matched analytical counties;
- 7 cartographic-only counties;
- 990 backcast-eligible counties.

## Reproducibility rule

The Stata master pipeline defines the analytical results. The Python cartography script reads the frozen Stata county outputs and produces the publication maps from those values.
