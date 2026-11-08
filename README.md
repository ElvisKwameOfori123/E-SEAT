# E-SEAT

## Ethanol Spatial Exposure and Agricultural Transition

**What happens to land use when a policy-driven demand signal weakens?**

**E-SEAT** is the reproducible empirical framework accompanying:

> **Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt**

The study examines how county-level corn specialization in the U.S. Midwest may adjust when the national corn-ethanol demand signal weakens. It separates **estimated responsiveness** from **starting specialization** and evaluates how those features shape persistent spatial differences.

## In foresight terms

Transitions are rarely a clean reversal of the forces that created them. E-SEAT reads a past
transition to learn how land use adjusts when a policy-made demand signal fades: which places
respond, which stay locked in, and how starting specialization and soil shape the difference. Its
scenario backcast removes the estimated ethanol-demand component step by step, a stress-test of how
persistent the corn landscape is. The lesson carries to other agricultural transitions in which a
long-standing demand signal may weaken: anticipating change includes anticipating lock-in.

## Part of a strategic foresight system

Strategic foresight is the ability to perceive, make sense of and act upon different ideas of the
future emerging in the present (OECD, 2021). These repositories form one such system for
anticipating the transition of Irish agriculture; each plays one role.

| Role | Repository | Question it answers |
|---|---|---|
| Perceive: signals of change | GOBLIN-Spatial | How have livestock systems changed in every place, 2015–2025? |
| Perceive: the present, farm by farm | AgriSyn v2 | Which farms, of what kind, are where today? |
| Make sense: a shared view | GOBLIN-Spatial Explorer | What does that change look like for a place, county or catchment? |
| Act: test instruments | StockRate-Sim | How would farms respond to a livestock tax or a tradable cap? |
| Act: stress-test a pathway | AgriSyn NZ | Who carries the 2050 net-zero land transition? |
| **Learn: a past transition** | **E-SEAT (this repository)** | **Does land use lock in when a demand signal weakens? (US Corn Belt)** |

*OECD (2021), Towards a strategic foresight system in Ireland, OECD Policy Brief.*

## Study coverage

E-SEAT covers counties in Illinois, Indiana, Iowa, Kansas, Michigan, Minnesota, Missouri, Nebraska, North Dakota, Ohio, South Dakota, and Wisconsin across six Census of Agriculture waves: **1997, 2002, 2007, 2012, 2017, and 2022**.

| Replication checkpoint | Value |
| --- | ---: |
| Counties in analytical data spine | 1,048 |
| Potential county-year observations | 6,288 |
| Principal corn-share observations | 5,977 |
| Counties in principal corn-share model | 1,005 |
| Backcast-eligible counties | 990 |

## Analytical workflow

The replication sequence is:

**source data → data preparation → county panel → fixed-effects estimation → county sensitivity → scenario backcasting → robustness checks → frozen county outputs → publication maps**

The principal outcome is harvested corn acreage as a percentage of agricultural land. The main fixed-effects specification interacts the national corn-ethanol demand trajectory with two predetermined county characteristics:

- 1997 corn specialization
- NCCPI soil productivity

County and Census-year fixed effects are included. The interaction terms identify **differential county responses** to the common national ethanol-demand trajectory; they do not identify the aggregate national effect of ethanol demand.

The backcast begins from observed 2022 county corn shares and progressively removes the estimated **differential ethanol-demand component**. Complete removal is a diagnostic boundary case and does not represent elimination of the ethanol market.

## Reproducing the analysis

Start with:

1. `data/README.md` for required inputs and provenance.
2. `data/MANIFEST.csv` for the input inventory.
3. `code/stata/FINAL_ECOLEC_R1_MASTER.do` for the analytical sequence.
4. `code/python/FINAL_ECOLEC_R1_PUBLICATION_MAPS.py` for publication maps generated from frozen Stata county outputs.

**StataNow 18.5 is the authoritative analytical environment.** Python is used only to render maps from frozen Stata outputs and does not re-estimate the statistical models or reconstruct the backcast.

Source suppression and unavailable values are retained as missing rather than mechanically recoded to zero.

## Data provenance

The E-SEAT database combines USDA Census of Agriculture data, national corn and ethanol-use series, NCCPI soil productivity, county population and spatial data, ethanol-processing information, and selected public research materials.

Selected data and estimation materials from the public [galvez-soriano/Papers/EthanolCorn](https://github.com/galvez-soriano/Papers/tree/main/EthanolCorn) repository associated with Hoanh Le and Oscar Gálvez-Soriano were used as upstream source material and combined with additional official and independently assembled inputs.

Detailed provenance and preparation notes are provided in:

- `data/README.md`
- `data/MANIFEST.csv`
- `documentation/DATA_PREPARATION.md`

Original source datasets remain subject to the redistribution and attribution requirements of their providers.

## Repository status

This repository contains the Revision 1 reproducibility materials for the manuscript. The data-preparation module, provenance documentation, publication-map renderer, integrity checks, and release checklist are included. Remaining frozen analytical modules should be added before the repository is described as a complete one-command replication package.

Release checks are tracked in `RELEASE_CHECKLIST.md`.

## Citation

Ofori, E. K. (2026). **E-SEAT: Ethanol Spatial Exposure and Agricultural Transition framework.** Reproducible research materials for *Fuel-Market Reform and Structural Land-Use Lock-in in the U.S. Corn Belt*.

A machine-readable citation is provided in `CITATION.cff`.

## Acknowledgements

Source attribution and acknowledgements are provided in `ACKNOWLEDGEMENTS.md`.

## License

Repository code is released under the **MIT License**. Source datasets and spatial files remain subject to the terms and attribution requirements of their original providers.
