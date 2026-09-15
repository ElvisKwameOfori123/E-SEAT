# E-SEAT Public Release Checklist

This checklist defines the minimum package required before the repository is made public and cited as the replication archive for **Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt**.

## Repository documentation

- [x] README aligned with final manuscript terminology
- [x] MIT LICENSE present
- [x] CITATION.cff present
- [ ] data/README.md with acquisition, provenance, and redistribution notes
- [ ] documentation/reproducibility.md with exact run order and software requirements

## Authoritative analytical code

- [ ] code/stata/FINAL_ECOLEC_R1_MASTER.do
- [ ] Verify that the public script contains no user-specific absolute paths
- [ ] Verify package dependencies and installation instructions
- [ ] Verify all hard QA assertions against the frozen R1 results

## Publication cartography

- [ ] code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py
- [ ] Verify that Python reads only frozen Stata county outputs
- [ ] Verify that Python does not re-estimate analytical quantities
- [ ] Verify 2023 Census Cartographic Boundary geometry and FIPS join

## Frozen outputs

- [ ] Main regression table
- [ ] Event-style dynamics table and figure inputs
- [ ] Scenario assumptions and state summaries
- [ ] Backcast classifications
- [ ] Alternative reference-point sensitivity
- [ ] Asymmetric reversibility outputs
- [ ] Backcast group profiles
- [ ] Residual-gap summaries
- [ ] Current-plant and state-cluster robustness outputs
- [ ] Frozen county-level values used for publication maps

## Data handling

- [ ] Do not publish source files whose redistribution terms are uncertain
- [ ] Provide source links/acquisition instructions instead
- [ ] Include the Ohio 2022 correction provenance and reconciliation
- [ ] Confirm that suppressed Census values remain missing rather than zero-filled

## Final reconciliation

- [ ] 1,048 counties in analytical data spine
- [ ] 6 Census waves and 6,288 potential county-year rows
- [ ] 5,977 observations and 1,005 counties in principal corn-share model
- [ ] 990 backcast-eligible counties
- [ ] Backcast classes reconcile to 439 / 14 / 17 / 37 / 483
- [ ] Figures and tables reproduce the manuscript exactly
- [ ] README result values match the final manuscript
- [ ] Repository contains no credentials, private paths, temporary files, or restricted data
- [ ] Make repository public only after all checks above pass
