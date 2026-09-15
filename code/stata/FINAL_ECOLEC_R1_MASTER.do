/*******************************************************************************
E-SEAT: ETHANOL SPATIAL EXPOSURE AND AGRICULTURAL TRANSITION
Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt
ECOLEC-D-26-03083 | Revision 1 replication master

Author: Elvis Kwame Ofori
Software: StataNow 18.5

This public controller and its modules were reconstructed from the frozen
successful Revision 1 Stata command log and checked against the frozen R1
outputs. Analytical commands are preserved; the public setup is made portable
and the source assembly is described as data preparation.

Run from repository root:
    do code/stata/FINAL_ECOLEC_R1_MASTER.do

Optional custom input/output directories:
    do code/stata/FINAL_ECOLEC_R1_MASTER.do "path/to/input_data" "path/to/output"

Default input directory: data/local
Default output directory: outputs/r1

IMPORTANT: the backcast removes only the estimated county-specific DIFFERENTIAL
ethanol-demand component. Census-year fixed effects absorb the common national
component. This is not a literal zero-ethanol or general-equilibrium simulation.
*******************************************************************************/

version 18.5
clear all
set more off
set varabbrev off
capture log close _all

args datadir outputdir
if `"`datadir'"' == "" local datadir "data/local"
if `"`outputdir'"' == "" local outputdir "outputs/r1"

global root     `"`datadir'"'
global outdir   `"`outputdir'"'
global interdir "$outdir/intermediate"
global tabledir "$outdir/tables"
global sterdir  "$outdir/estimates"
global qadir    "$outdir/qa"
global subdir   "$outdir/submission_ready"
global maproot  "$outdir/map_geometry"
global mapsrc   "$maproot/source"
global mapdata  "$maproot/data"

* Default parent folder; custom output parents should already exist.
capture mkdir "outputs"
foreach d in "$outdir" "$interdir" "$tabledir" "$sterdir" "$qadir" "$subdir" "$maproot" "$mapsrc" "$mapdata" {
    capture mkdir `"`d'"'
}

log using "$outdir/R1_corn_ethanol_run.log", text replace

di as result "============================================================"
di as result "FUEL-MARKET REFORM AND CORN-BELT LAND-USE SPECIALIZATION"
di as result "ECOLEC-D-26-03083 -- REVISION 1 FINAL MASTER PIPELINE"
di as result "Start: `c(current_date)' `c(current_time)'"
di as result "Output folder: $outdir"
di as result "============================================================"

*-------------------------------------------------------------------------------
* 1.2 Input files
*-------------------------------------------------------------------------------

global agdb       "$root/AgDBase.dta"
global censusraw  "$root/CensusofAgData.dta"
global ohio2022   "$root/prepared/ohio_2022_corn_govpayment_prepared.csv"
global plants     "$root/EthanolPlantsatCounties.dta"
global cornqp     "$root/CornQP.dta"
global extmargin  "$root/ext_margin.dta"
global cornpc     "$root/CornPC.dta"

* Publication maps use the official 2023 Census Cartographic Boundary county
* file at 1:500,000 scale for the 12 study states.
global cbzip      "$root/cb_2023_midwest_counties_500k.zip"

foreach f in "$agdb" "$censusraw" "$ohio2022" "$plants" "$cornqp" "$extmargin" "$cornpc" "$cbzip" {
    capture confirm file "`f'"
    if _rc {
        di as error "Required file not found: `f'"
        log close
        exit 601
    }
}

*-------------------------------------------------------------------------------
* 1.3 Packages
*-------------------------------------------------------------------------------

foreach pkg in ftools reghdfe estout shp2dta {
    capture which `pkg'
    if _rc {
        di as text "Installing `pkg' from SSC"
        ssc install `pkg', replace
    }
}

*-------------------------------------------------------------------------------
* 1.4 Build matched Census cartographic map geometry
*-------------------------------------------------------------------------------
* The cartographic file is converted inside the pipeline with shp2dta. The
* resulting database and coordinate files receive a new _ID, while analytical
* values are joined by county FIPS. Spatial processing changes display geometry
* only and does not alter statistical values.

local __oldpwd "`c(pwd)'"
cd "$mapsrc"
unzipfile "$cbzip", replace

capture confirm file "$mapsrc/cb_2023_midwest_counties_500k.shp"
if _rc {
    di as error "Cartographic boundary shapefile not found after unzip."
    cd "`__oldpwd'"
    log close
    exit 601
}

shp2dta using "cb_2023_midwest_counties_500k", ///
    database("$mapdata/cb_2023_midwest_counties_500k_db") ///
    coordinates("$mapdata/cb_2023_midwest_counties_500k_coord") ///
    genid(_ID) replace

cd "`__oldpwd'"

global cb_db    "$mapdata/cb_2023_midwest_counties_500k_db.dta"
global cb_coord "$mapdata/cb_2023_midwest_counties_500k_coord.dta"

foreach f in "$cb_db" "$cb_coord" {
    capture confirm file "`f'"
    if _rc {
        di as error "Cartographic map dataset not created: `f'"
        log close
        exit 601
    }
}

* Geometry integrity check: the supplied Midwest file contains 1,055 counties
* across the 12 study states.
use "$cb_db", clear
capture confirm variable GEOID
if _rc {
    di as error "GEOID is missing from the Census cartographic database."
    log close
    exit 111
}
count
assert r(N) == 1055
di as result "Census cartographic map geometry ready: " r(N) " counties."

*-------------------------------------------------------------------------------
* 1.5 Study parameters
*-------------------------------------------------------------------------------

global corn_share_reference 20
global eps_sensitivity 0.001

global w_corn    0.35
global w_crop    0.15
global w_ethanol 0.20
global w_plants  0.10
global w_ext     0.10
global w_nccpi   0.10

global map_width  3000
global map_height 2000

di as result "Part 1 complete: setup, folders, files, packages, and log checked."

*-------------------------------------------------------------------------------
* Execute analytical modules in frozen R1 order
*-------------------------------------------------------------------------------
do "code/stata/modules/01_prepare_panel.do"
do "code/stata/modules/02_main_event_exposure.do"
do "code/stata/modules/03_robustness_scenarios.do"
do "code/stata/modules/04_backcast_diagnostics.do"
do "code/stata/modules/05_backcast_profiles.do"
do "code/stata/modules/06_freeze_outputs.do"

* Frozen headline reconciliation.
use "$outdir/final_county_outputs_for_maps_and_tables.dta", clear
quietly count if backcast_eligible == 1
assert r(N) == 990
quietly count if backcast_eligible == 1 & backcast_class == 1
assert r(N) == 439
quietly count if backcast_eligible == 1 & backcast_class == 2
assert r(N) == 14
quietly count if backcast_eligible == 1 & backcast_class == 3
assert r(N) == 17
quietly count if backcast_eligible == 1 & backcast_class == 4
assert r(N) == 37
quietly count if backcast_eligible == 1 & backcast_class == 5
assert r(N) == 483
noi di as result "Frozen E-SEAT R1 headline checks passed: 439 / 14 / 17 / 37 / 483."

capture log close
