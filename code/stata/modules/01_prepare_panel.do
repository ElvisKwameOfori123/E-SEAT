/* E-SEAT R1 module: 01_prepare_panel.do
   Reconstructed from the frozen successful Revision 1 Stata command log.
   Called by FINAL_ECOLEC_R1_MASTER.do; do not run standalone unless globals are set. */

/*******************************************************************************
* PART 2. PANEL PREPARATION AND SOURCE ALIGNMENT
*
* The row-balanced 1,048-county x 6-wave panel is retained as the data spine.
* Estimation samples are allowed to become unbalanced where Census values are
* genuinely suppressed or unavailable. Missing values are NEVER recoded to zero.
*******************************************************************************/

use "$agdb", clear

di as text "Master panel loaded."
describe
summarize

keep if inlist(Year, 1997, 2002, 2007, 2012, 2017, 2022)

* Ensure numeric FIPS key.
capture confirm numeric variable fips_code
if _rc {
    capture confirm string variable fips
    if !_rc {
        gen str20 fips_clean = trim(fips)
        destring fips_clean, gen(fips_code) force
        drop fips_clean
    }
}
replace fips_code = round(fips_code)
drop if missing(fips_code)

* Validate the row grid. This is a balanced DATA SPINE, not necessarily a
* balanced estimation sample after correct treatment of suppressed values.
isid fips_code Year
bysort fips_code: gen __n_years = _N
tab __n_years
assert __n_years == 6
drop __n_years

quietly count
local N_panel = r(N)
quietly levelsof fips_code, local(__counties)
local N_counties : word count `__counties'
di as result "Panel spine confirmed: `N_counties' counties and `N_panel' county-year rows."

*-------------------------------------------------------------------------------
* 2.1 Restore source Census missingness before county-level source alignment
*-------------------------------------------------------------------------------
*
* AgDBase contains downstream zero-filled values for corn_share and government
* payments. CensusofAgData.dta preserves the raw missingness. Re-attach the raw
* harvested-corn acreage and GovPayment fields first, then incorporate Ohio 2022 values from
* the official USDA county tables.
preserve
    use "$censusraw", clear
    keep if inlist(Year, 1997, 2002, 2007, 2012, 2017, 2022)

    capture confirm numeric variable fips_state
    if _rc {
        destring fips_state, gen(__state_num) force
    }
    else {
        gen double __state_num = fips_state
    }

    capture confirm numeric variable fips_cnty
    if _rc {
        destring fips_cnty, gen(__county_num) force
    }
    else {
        gen double __county_num = fips_cnty
    }

    gen long fips_code = 1000*__state_num + __county_num
    drop __state_num __county_num
    drop if missing(fips_code)

    keep fips_code Year TotalCornAreaHarvested GovPayment
    rename TotalCornAreaHarvested raw_TotalCornAreaHarvested
    rename GovPayment raw_GovPayment

    isid fips_code Year
    tempfile census_core_raw
    save `census_core_raw', replace
restore

merge 1:1 fips_code Year using `census_core_raw', gen(_merge_censusraw)
tab _merge_censusraw
assert _merge_censusraw == 3

* Restore raw values INCLUDING missing values.
replace TotalCornAreaHarvested = raw_TotalCornAreaHarvested
replace GovPayment             = raw_GovPayment
drop raw_TotalCornAreaHarvested raw_GovPayment _merge_censusraw

*-------------------------------------------------------------------------------
* 2.2 Integrate Ohio 2022 values from official county tables
*-------------------------------------------------------------------------------
*
* Source preparation:
*   Corn: USDA 2022 Census of Agriculture, Ohio County Table 24.
*         86 observed counties; Belmont (39013) and Cuyahoga (39035) are (D).
*   GovPayment: USDA 2022 Census of Agriculture, Ohio County Table 5.
*         All 88 county totals are reported in $1,000; the prepared table stores
*         GovPayment_2022 in dollars to match the panel variable.
preserve
    import delimited using "$ohio2022", clear varnames(1)
    keep fips_code Year corn_acres_harvested_2022 corn_status GovPayment_2022 govpay_status
    isid fips_code Year
    tempfile ohio2022_prepared
    save `ohio2022_prepared', replace
restore

merge 1:1 fips_code Year using `ohio2022_prepared', ///
    keepusing(corn_acres_harvested_2022 corn_status GovPayment_2022 govpay_status) ///
    gen(_merge_ohio)

tab _merge_ohio
assert _merge_ohio != 2
quietly count if _merge_ohio == 3
assert r(N) == 88

replace TotalCornAreaHarvested = corn_acres_harvested_2022 ///
    if _merge_ohio == 3 & corn_status == "observed"

replace TotalCornAreaHarvested = . ///
    if _merge_ohio == 3 & corn_status == "D_suppressed"

replace GovPayment = GovPayment_2022 ///
    if _merge_ohio == 3 & govpay_status == "observed"

* Source-coverage and unit QA for Ohio 2022.
quietly summarize TotalCornAreaHarvested if statefp == 39 & Year == 2022, meanonly
di as result "Ohio 2022 observed county corn-acre sum = " %12.0fc r(sum)
assert abs(r(sum) - 3313863) < 0.5

quietly count if statefp == 39 & Year == 2022 & missing(TotalCornAreaHarvested)
di as result "Ohio 2022 counties with suppressed corn acreage = " r(N)
assert r(N) == 2

quietly summarize GovPayment if statefp == 39 & Year == 2022, meanonly
di as result "Ohio 2022 county government-payment sum, dollars = " %15.0fc r(sum)
assert abs(r(sum) - 136764000) < 0.5

drop corn_acres_harvested_2022 corn_status GovPayment_2022 govpay_status _merge_ohio

*-------------------------------------------------------------------------------
* 2.3 Construct analytical variables from prepared source fields
*-------------------------------------------------------------------------------

capture drop corn_share crop_intensity log_land_value log_govpay_acre ///
    AnnualReturn_mi_clean AnnualReturn_mi_final

* [C3, C12, C13] Main corn outcome is HARVESTED corn acreage divided by TOTAL
* agricultural land. Missing harvested acreage remains missing.
gen double corn_share = 100 * TotalCornAreaHarvested / TotalArea ///
    if TotalArea > 0 & !missing(TotalCornAreaHarvested)
label var corn_share "Harvested corn share of agricultural land, percent"

* Retain the legacy variable only for forensic comparison. It is not used.
capture label var PecentPlantedCorn "LEGACY zero-filled corn-share series; not used in the prepared R1 analysis"

gen crop_intensity = pct_cropland
label var crop_intensity "Cropland share of agricultural land, percent"

gen log_land_value = log(LandValue) if LandValue > 0
label var log_land_value "Log land value"

* Construct government-payment derivatives from the source-consistent value.
capture confirm variable GovPay
if !_rc {
    replace GovPay = GovPayment
}

capture confirm variable GovPay_mi
if !_rc {
    replace GovPay_mi = GovPayment / 1000000
}

capture confirm variable Gov_dollarperacre
if _rc {
    gen double Gov_dollarperacre = .
}
else {
    replace Gov_dollarperacre = .
}

replace Gov_dollarperacre = GovPayment / TotalArea ///
    if TotalArea > 0 & !missing(GovPayment)

gen log_govpay_acre = log(Gov_dollarperacre + 1) ///
    if !missing(Gov_dollarperacre)
label var log_govpay_acre "Log government payment per acre plus one"

gen AnnualReturn_mi_clean = AnnualReturn / 1000 if !missing(AnnualReturn)
label var AnnualReturn_mi_clean "Annual return, millions"

gen AnnualReturn_mi_final = AnnualReturn_mi_clean
label var AnnualReturn_mi_final "Annual return, millions"


/*******************************************************************************
* PART 2B. DATA-PREPARATION QA (Q1-Q3 + GOVERNMENT PAYMENTS)
*
* These checks verify source coverage, missingness, units, and denominator choices.
* All estimates are generated from the prepared variables above.
*******************************************************************************/

di _n as result "=========== PART 2B: DATA-PREPARATION QA ==========="

capture log close qa
log using "$qadir/qa_audit_data_preparation.txt", text replace name(qa)

* Q1. Provenance and denominator.
di _n as result "--- Q1. CORN PROVENANCE AND DENOMINATOR ---"

capture drop __share_agland __share_cropland __diff_agland
gen double __share_agland   = 100 * TotalCornAreaHarvested / TotalArea ///
    if TotalArea > 0 & !missing(TotalCornAreaHarvested)
gen double __share_cropland = 100 * TotalCornAreaHarvested / CroplandArea ///
    if CroplandArea > 0 & !missing(TotalCornAreaHarvested)
gen double __diff_agland = corn_share - __share_agland

summarize corn_share __share_agland __share_cropland __diff_agland
quietly summarize __diff_agland if !missing(__diff_agland)
di as result "Max |constructed corn_share - harvested corn/ag land| = " ///
    max(abs(r(min)), abs(r(max)))

* Q2. Missing harvested acreage after source preparation.
di _n as result "--- Q2. SOURCE-CONSISTENT MISSING CORN ACREAGE ---"
gen byte __acres_missing = missing(TotalCornAreaHarvested)

tab Year __acres_missing, row
tab State_str __acres_missing, row

count if Year == 2022 & __acres_missing == 1
di as result "2022 counties with missing harvested corn acreage after preparation = " r(N)

count if statefp == 39 & Year == 2022 & __acres_missing == 1
di as result "Ohio 2022 missing after preparation = " r(N) " (expected: Belmont and Cuyahoga)"
assert r(N) == 2

list State_str County_str fips_code Year if statefp == 39 & Year == 2022 & __acres_missing == 1, ///
    clean noobs

preserve
    keep if __acres_missing == 1
    keep fips fips_code State_str County_str Year TotalCornAreaHarvested corn_share
    capture export excel using "$qadir/qa_missing_corn_rows_after_preparation.xlsx", ///
        firstrow(variables) replace
restore

* Q3. Denominator diagnostic, prepared 2022 sample.
di _n as result "--- Q3. AGRICULTURAL LAND VS CROPLAND DENOMINATOR ---"

summarize corn_share __share_cropland crop_intensity if Year == 2022, detail

count if Year == 2022 & !missing(corn_share) & corn_share <= 20
di as result "Observed 2022 counties <=20%, agricultural-land denominator = " r(N)

count if Year == 2022 & !missing(__share_cropland) & __share_cropland <= 20
di as result "Observed 2022 counties <=20%, cropland denominator = " r(N)

corr corn_share __share_cropland if Year == 2022

preserve
    keep if Year == 2022
    keep fips_code State_str County_str corn_share __share_cropland crop_intensity
    rename __share_cropland corn_share_of_cropland
    capture export excel using "$qadir/qa_Q3_denominator_comparison_2022.xlsx", ///
        firstrow(variables) replace
restore

* Government-payment source coverage.
di _n as result "--- GOVERNMENT PAYMENT MISSINGNESS AFTER REPAIR ---"
tab Year if missing(GovPayment)
tab State_str if missing(GovPayment)

count if statefp == 39 & Year == 2022 & missing(GovPayment)
di as result "Ohio 2022 missing government-payment totals after preparation = " r(N)
assert r(N) == 0

* Annual return availability.
di _n as result "--- ANNUAL RETURN AVAILABILITY ---"
tab Year if missing(AnnualReturn)
count if Year == 2022 & missing(AnnualReturn)
di as result "2022 rows missing AnnualReturn = " r(N)

capture drop __share_agland __share_cropland __diff_agland __acres_missing
log close qa

di as result "Part 2B complete: data-preparation audit written to $qadir"

*-------------------------------------------------------------------------------
* 2.4 Predetermined 1997 exposure
*-------------------------------------------------------------------------------

preserve
    keep if Year == 1997
    keep fips_code corn_share nccpi
    rename corn_share base_corn_share_1997
    rename nccpi base_nccpi_1997
    label var base_corn_share_1997 "Corn share in 1997, predetermined baseline"
    label var base_nccpi_1997 "Time-invariant NCCPI, baseline soil productivity"
    isid fips_code
    save "$interdir/base_1997_exposure.dta", replace
restore

merge m:1 fips_code using "$interdir/base_1997_exposure.dta"
tab _merge
drop if _merge == 2
drop _merge

quietly count if missing(base_corn_share_1997)
di as result "County-year rows with missing 1997 corn baseline = " r(N)
quietly count if Year == 1997 & missing(base_corn_share_1997)
di as result "Counties with missing 1997 corn baseline = " r(N)

assert !missing(base_nccpi_1997)

*-------------------------------------------------------------------------------
* 2.5 National ethanol-demand series
*-------------------------------------------------------------------------------

preserve
    use "$cornqp", clear

    capture confirm variable Year
    if _rc {
        capture confirm variable year
        if !_rc rename year Year
    }

    capture confirm variable ethanoluse
    if _rc {
        di as error "CornQP is missing ethanoluse."
        exit 111
    }

    capture confirm variable totalproduction
    if _rc {
        di as error "CornQP is missing totalproduction."
        exit 111
    }

    gen ethanol_share_production = 100 * ethanoluse / totalproduction ///
        if totalproduction > 0
    label var ethanol_share_production ///
        "National ethanol use as share of corn production, percent"

    capture confirm variable pricesreceivedbyfarmersdollarspe
    if !_rc rename pricesreceivedbyfarmersdollarspe corn_price_bu

    capture confirm variable corn_price_bu
    if _rc gen corn_price_bu = .

    keep Year ethanol_share_production corn_price_bu
    duplicates drop Year, force
    isid Year

    save "$interdir/national_ethanol_share.dta", replace
restore

merge m:1 Year using "$interdir/national_ethanol_share.dta"
tab _merge
drop if _merge == 2
drop _merge

assert !missing(ethanol_share_production)

* Clean causal interactions. No plant count in the main model.
capture drop basecorn_x_E nccpi_x_E totalplant_x_E plant_x_E

gen basecorn_x_E = base_corn_share_1997 * ethanol_share_production
label var basecorn_x_E "1997 corn share × national ethanol share"

gen nccpi_x_E = base_nccpi_1997 * ethanol_share_production
label var nccpi_x_E "Baseline NCCPI × national ethanol share"

* Robustness only.
replace totalplant = 0 if missing(totalplant)
replace ethanol_plant = 0 if missing(ethanol_plant)

gen totalplant_x_E = totalplant * ethanol_share_production
label var totalplant_x_E "Current plant count × national ethanol share, robustness only"

gen plant_x_E = ethanol_plant * ethanol_share_production
label var plant_x_E "Current plant presence × national ethanol share, robustness only"

* Missingness diagnostics.
foreach v in corn_share crop_intensity log_land_value log_govpay_acre ///
    AnnualReturn_mi_final base_corn_share_1997 base_nccpi_1997 ///
    ethanol_share_production PopDen {
    quietly count if missing(`v')
    di as text "Missing `v': " r(N)
}

xtset fips_code Year
save "$interdir/analysis_panel_clean.dta", replace

di as result "Part 2 complete: prepared analysis panel saved."
