---
title: UKESM1 Release Notes
---
These are the notes for UKESM1, the first release of the UK Earth System Model. Some background information on the model, its components and the prerequisites for using it can be found in the [introduction to UKESM](/_unified-model/configurations/ukesm.md).

UKESM1.1 is a later release of UKESM.  Its release notes are [here](relnotes-1.1.md).

## Model Configurations

The model is available in a number of configurations for running different types of experiment:

* [Atmosphere-only](relnotes-1.0/amip.md):
The so-called **AMIP** configuration, in which the model atmosphere is forced by observed sea surface temperature and sea ice boundary conditions.

* [Coupled](relnotes-1.0/coupled.md):
Two fully coupled configurations, which each make use of all model components:
  * one set up to run the CMIP6 **pre-industrial** control experiment, and
  * one to run the CMIP6 **historical** experiment.

There are also additional coupled configurations for the CMIP6 **abrupt4xCO2** and **1%CO2** experiments, which can be created using the pre-industrial control experiment as a starting point.

A full description of how to access and run each configuration can be found on the [AMIP](relnotes-1.0/amip.md) and [Coupled](relnotes-1.0/coupled.md) configuration pages.

## CMIP6 Data

Datasets from CMIP6 experiments run using UKESM1 are available from the Earth System Grid Federation (ESGF).  Full details are available from the following Digital Object Identifiers (DOIs):

| Experiment | DOI |
| DECK | https://doi.org/10.22033/ESGF/CMIP6.1569 |
| Historical | https://doi.org/10.22033/ESGF/CMIP6.6113 |
| ScenarioMIP - ssp119 |	https://doi.org/10.22033/ESGF/CMIP6.6329 |
| ScenarioMIP - ssp126 | https://doi.org/10.22033/ESGF/CMIP6.6333 |
| ScenarioMIP - ssp245 | https://doi.org/10.22033/ESGF/CMIP6.6339	|
| ScenarioMIP - ssp370 | https://doi.org/10.22033/ESGF/CMIP6.6347 |
| ScenarioMIP - ssp434 | https://doi.org/10.22033/ESGF/CMIP6.6389	|
| ScenarioMIP - ssp534-over | https://doi.org/10.22033/ESGF/CMIP6.6397	|
| ScenarioMIP - ssp585 | 	https://doi.org/10.22033/ESGF/CMIP6.6405	|

## Support
* NERC users requiring assistance running this suite on NERC machines (ARCHER, NEXCS, Monsoon) should raise a ticket on the [NCAS-CMS helpdesk](https://cms-helpdesk.ncas.ac.uk).
* Users running this suite on other machines should contact local support services.

