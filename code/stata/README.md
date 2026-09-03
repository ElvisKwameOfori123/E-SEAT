# Stata pipeline

The final E-SEAT analysis is executed from the frozen Revision 1 master Stata script.

The repository version will preserve the empirical specification and numerical logic of `FINAL_ECOLEC_R1_MASTER.do` while replacing the local absolute project path with a portable repository path configuration.

The master run creates timestamped output directories and performs hard quality-assurance checks before completing.

Required Stata version: **StataNow 18.5**.

User-written packages used by the final pipeline: `ftools`, `reghdfe`, `estout`, `spmap`, `coefplot`, and `shp2dta`.
