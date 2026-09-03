# Python cartography

The E-SEAT Python component renders publication-quality county maps from frozen Stata outputs.

The final script uses the 2023 U.S. Census Cartographic Boundary county geometry and joins analytical values by FIPS/GEOID.

Expected Python packages: `numpy`, `pandas`, `geopandas`, `matplotlib`, `shapely`, and `pyogrio`.

The frozen Revision 1 mapping workflow checks:

- 1,055 spatial counties;
- 1,048 matched analytical counties;
- 990 backcast-eligible counties; and
- backcast class counts of 439 / 14 / 17 / 37 / 483.

The final script will be copied from the frozen Revision 1 file after the repository path is made portable.
