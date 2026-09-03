# Quality assurance

E-SEAT treats replication checks as part of the analytical workflow rather than as separate presentation material.

The final Revision 1 pipeline checks:

- uniqueness of county FIPS-year observations;
- the 1,048-county × 6-wave panel spine;
- restoration of raw Census missingness;
- the Ohio 2022 correction totals and suppression count;
- merge integrity across analytical inputs;
- Census cartographic geometry size and FIPS matching;
- the corrected backcast-eligible sample;
- frozen transition-class counts; and
- consistency of exported county values used in publication maps.

The public release will retain machine-readable QA outputs sufficient to confirm that a replication run reproduces the frozen analytical sample and reported classifications.
