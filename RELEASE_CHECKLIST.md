# E-SEAT Public Release Checklist

This checklist defines the minimum package required before the repository is made public and cited as the replication archive for **Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt**.

## Repository documentation

- [x] README aligned with final manuscript terminology
- [x] Data-preparation logic documented without post-hoc repair framing
- [x] MIT LICENSE present
- [x] CITATION.cff present
- [x] data/README.md with provenance, preparation, integrity, and redistribution notes
- [x] data/MANIFEST.csv with byte sizes and SHA-256 digests
- [ ] documentation/reproducibility.md with exact run order and software requirements

## Authoritative analytical code

- [x] code/stata/FINAL_ECOLEC_R1_MASTER.do controller added
- [x] code/stata/modules/01_prepare_panel.do added
- [ ] Add remaining frozen Stata analytical modules
- [x] Verify that public scripts contain no user-specific absolute paths
- [x] Verify package dependencies and installation instructions
- [ ] Verify all hard QA assertions against frozen R1 results

## Publication cartography

- [x] Recover and add the original code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py
- [x] Do not substitute a newly invented renderer for the original script
- [x] Verify that Python reads only frozen Stata county outputs
- [x] Verify that Python does not re-estimate analytical quantities
- [x] Verify 2023 Census Cartographic Boundary geometry and FIPS join

## Data handling

- [x] Preserve source suppression as missing rather than zero
- [x] Document the 2022 Ohio county-table preparation and source coverage
- [x] Store the public Ohio preparation table under data/prepared/
- [x] Provide public text mirrors of CornQP, CornPC, ethanol-plant, and extensive-margin inputs
- [x] Provide a local input-integrity verification script
- [ ] Check redistribution terms before making original binary source files public

## Final reconciliation

- [x] 1,048 counties in analytical data spine
- [x] 6 Census waves and 6,288 potential county-year rows
- [x] 5,977 observations and 1,005 counties in principal corn-share model
- [x] 990 backcast-eligible counties
- [x] Backcast classes reconcile to 439 / 14 / 17 / 37 / 483
- [ ] Figures and tables reproduce the manuscript exactly
- [x] README result values match the frozen R1 analytical results
- [ ] Repository contains no credentials, private paths, temporary files, or restricted data
- [ ] Make repository public only after all checks above pass
