---
title: UKESM1.1 Release Notes
teaser: These are the notes for UKESM1.1, the latest release of the UK Earth System Model. Some background information on the model, its components and the prerequisites for using it can be found in the <a href="https:/cms.ncas.ac.uk/unified-model/configurations/ukesm">introduction to UKESM</a>.
---

The first release of UKESM is also available.  See the [UKESM1 release notes](../relnotes-1.0).

## Model Configurations

The model is available in a number of configurations for running different types of experiment:

* [Atmosphere-only](amip):
The so-called **AMIP** configuration, in which the model atmosphere is forced by observed sea surface temperature and sea ice boundary conditions.

* [Coupled](coupled):
Two fully coupled configurations, which each make use of all model components:
  * one set up to run the CMIP6 **pre-industrial** control experiment, and
  * one to run the CMIP6 **historical** experiment.

There are also additional coupled configurations for the CMIP6 **abrupt4xCO2** and **1%CO2** experiments, which can be created using the pre-industrial control experiment as a starting point.

A full description of how to access and run each configuration can be found on the [AMIP](amip) and [Coupled](coupled) configuration pages.

## CMIP6 Data

Datasets from CMIP6 experiments run using UKESM1.1 are available from the Earth System Grid Federation (ESGF).  Full details are available from the following Digital Object Identifiers (DOIs):

| Experiment | DOI |
| DECK | [https://doi.org/10.22033/ESGF/CMIP6.16781](https://doi.org/10.22033/ESGF/CMIP6.16781) |
| Historical | [https://doi.org/10.22033/ESGF/CMIP6.16797](https://doi.org/10.22033/ESGF/CMIP6.16797) |
| ScenarioMIP - ssp126 | [https://doi.org/10.22033/ESGF/CMIP6.16841](https://doi.org/10.22033/ESGF/CMIP6.16841) |
| ScenarioMIP - ssp370 | [https://doi.org/10.22033/ESGF/CMIP6.16845](https://doi.org/10.22033/ESGF/CMIP6.16845) |

## Support
* NERC users requiring assistance running this suite on NERC machines (ARCHER, NEXCS, Monsoon) should raise a ticket on the [NCAS-CMS helpdesk](https://cms-helpdesk.ncas.ac.uk).
* Users running this suite on other machines should contact local support services.

