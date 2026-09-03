# Spatial data

E-SEAT uses the official 2023 U.S. Census Cartographic Boundary county geometry at 1:500,000 scale for the twelve study states.

## Final geometry input

`cb_2023_midwest_counties_500k.zip`

The archive contains the county shapefile components used by the final Revision 1 pipeline:

- `.shp`
- `.dbf`
- `.shx`
- `.prj`
- `.cpg`

The file contains 1,055 counties across the twelve study states. Analytical county values are joined to geometry by county FIPS/GEOID.

## Mapping workflow

The Stata pipeline unpacks the cartographic boundary archive, converts it using `shp2dta`, creates a fresh map identifier, and checks the geometry count before map outputs are generated.

The final publication cartography reads frozen Stata county outputs and joins them to the same Census geometry by FIPS/GEOID.

## Integrity checkpoints

- Census geometry counties: 1,055
- E-SEAT analytical counties matched to geometry: 1,048
- cartographic-only counties: 7
- backcast-eligible analytical counties: 990
