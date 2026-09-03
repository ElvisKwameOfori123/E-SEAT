# Code

E-SEAT uses a Stata-centered analytical workflow with a separate Python cartography companion.

## `stata/`

The final master Stata pipeline is the authoritative source for:

- panel reconstruction and data corrections;
- variable construction;
- fixed-effects estimation;
- event-style dynamics;
- scenario translation;
- backcasting and classification;
- sensitivity analysis and quality assurance;
- tables, replication figures, and frozen county-level outputs.

## `python/`

The publication mapping script reads the frozen county-level outputs created by Stata and renders the final thematic maps using the Census 2023 cartographic boundary geometry.

The exact final scripts will be added from the frozen Revision 1 files after a filename and path portability pass. Analytical equations, coefficients, classifications, and county results will not be rewritten during that pass.
