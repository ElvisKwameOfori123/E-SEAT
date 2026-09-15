# E-SEAT data preparation

This note records the public replication logic used to move from source files to the analysis-ready county panel.

## 1. County data spine

E-SEAT begins from the assembled county agricultural panel and retains the six Census of Agriculture waves used in the study: 1997, 2002, 2007, 2012, 2017, and 2022. County FIPS is standardised and uniqueness is checked at the county-year level.

The resulting data spine contains 1,048 counties and 6,288 potential county-year observations. This is a structural frame for replication, not a claim that every outcome is observed in every county-year.

## 2. Source missingness

Harvested corn acreage and government-payment fields are reattached from the source Census data before analytical variables are constructed. Suppressed or unavailable source observations remain missing. They are not converted to zero.

This rule matters because corn specialization is defined from harvested acreage and because government payments are transformed on a per-acre basis. A suppressed source value cannot be interpreted as zero production or zero payment.

## 3. Ohio 2022 source-table preparation

The final analytical file uses 2022 Ohio harvested-corn and government-payment values assembled from the official USDA Census of Agriculture county tables.

The prepared table is stored as:

`data/prepared/ohio_2022_corn_govpayment_prepared.csv`

For harvested corn, 86 county values are observed. Belmont and Cuyahoga are source-suppressed and remain missing. Government-payment values are available for all 88 counties.

The workflow checks the observed harvested-corn total of 3,313,863 acres and the government-payment total of $136,764,000. These are source-coverage and unit-consistency checks.

## 4. Analytical variable construction

After source fields are aligned:

- corn specialization = harvested corn acreage / total agricultural land × 100;
- crop intensity is taken from the cropland share of agricultural land;
- log farmland value is constructed from positive land values;
- government payments per acre are rebuilt from the prepared government-payment field and total agricultural land;
- annual return is converted to the reporting units used in the manuscript.

Only after this step are predetermined county conditions and the national ethanol-demand series merged into the panel.

## 5. Predetermined conditions and national demand

The empirical design uses 1997 corn specialization as the starting production structure and time-invariant NCCPI as the soil-productivity gradient. National ethanol demand is measured as the share of U.S. corn production used for ethanol.

The fixed-effects models interact the national trajectory with the predetermined county gradients. Census-year fixed effects absorb the common national component, so the estimated coefficients describe differential county responses.

## 6. Spatial preparation

Spatial geometry is handled separately from the analytical values. Publication maps use the 2023 U.S. Census Cartographic Boundary county file at 1:500,000 scale. County outputs are joined to the geometry by FIPS/GEOID.

The geometry contains 1,055 counties across the twelve study states, of which 1,048 match the analytical county frame. Spatial processing affects display only and does not alter estimated values.

## 7. Division of labour between Stata and Python

Stata is the authoritative analytical pipeline. It performs data preparation, variable construction, estimation, dynamic analysis, scenarios, backcasting, robustness analysis, and export of frozen county-level map values.

Python is used only after those values have been frozen. The publication renderer joins the Stata-produced values to the Census geometry and draws the journal maps. It does not recalculate regressions, sensitivities, backcasts, or classifications.
