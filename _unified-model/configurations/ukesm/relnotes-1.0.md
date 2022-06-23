---
title: UKESM1 Release Notes
teaser: These are the notes for UKESM1, the first release of the UK Earth System Model. Some background information on the model, its components and the prerequisites for using it can be found in the <a href="https:/cms.ncas.ac.uk/unified-model/configurations/ukesm">introduction to UKESM</a>.
---

A later release, UKESM1.1 is avaiable, see the [UKESM1.1 release notes](../relnotes-1.1).

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
Datasets from CMIP6 experiments run using UKESM1 are available from the Earth System Grid Federation (ESGF).  Full details are available from the following Digital Object Identifiers (DOIs):

| Experiment | DOI |
| DECK | [https://doi.org/10.22033/ESGF/CMIP6.1569](https://doi.org/10.22033/ESGF/CMIP6.1569) |
| Historical | [https://doi.org/10.22033/ESGF/CMIP6.6113](https://doi.org/10.22033/ESGF/CMIP6.6113) |
| ScenarioMIP - ssp119 |	[https://doi.org/10.22033/ESGF/CMIP6.6329](https://doi.org/10.22033/ESGF/CMIP6.6329) |
| ScenarioMIP - ssp126 | [https://doi.org/10.22033/ESGF/CMIP6.6333](https://doi.org/10.22033/ESGF/CMIP6.6333) |
| ScenarioMIP - ssp245 | [https://doi.org/10.22033/ESGF/CMIP6.6339](https://doi.org/10.22033/ESGF/CMIP6.6339)	|
| ScenarioMIP - ssp370 | [https://doi.org/10.22033/ESGF/CMIP6.6347](https://doi.org/10.22033/ESGF/CMIP6.6347) |
| ScenarioMIP - ssp434 | [https://doi.org/10.22033/ESGF/CMIP6.6389](https://doi.org/10.22033/ESGF/CMIP6.6389)	|
| ScenarioMIP - ssp534-over | [https://doi.org/10.22033/ESGF/CMIP6.6397](https://doi.org/10.22033/ESGF/CMIP6.6397)	|
| ScenarioMIP - ssp585 | 	[https://doi.org/10.22033/ESGF/CMIP6.6405](https://doi.org/10.22033/ESGF/CMIP6.6405)	|

## Documentation
UKESM1 is documented in:

Alistair A. Sellar, Colin G. Jones, Jane P. Mulcahy, Yongming Tang, Andrew Yool, Andy Wiltshire, Fiona M. O'Connor, Marc Stringer, Richard Hill, Julien Palmieri, Stephanie Woodward, Lee de Mora, Till Kuhlbrodt, Steven T. Rumbold, Douglas I. Kelley, Rich Ellis, Colin E. Johnson, Jeremy Walton, Nathan Luke Abraham, Martin B. Andrews, Timothy Andrews, Alex T. Archibald, Ségolène Berthou, Eleanor Burke, Ed Blockley, Ken Carslaw, Mohit Dalvi, John Edwards, Gerd A. Folberth, Nicola Gedney, Paul T. Griffiths, Anna B. Harper, Maggie A. Hendry, Alan J. Hewitt, Ben Johnson, Andy Jones, Chris D. Jones, James Keeble, Spencer Liddicoat, Olaf Morgenstern, Robert J. Parker, Valeriu Predoi, Eddy Robertson, Antony Siahaan, Robin S. Smith, Ranjini Swaminathan, Matthew T. Woodhouse, Guang Zeng, Mohamed Zerroukat (2019). *UKESM1: Description and evaluation of the U.K. Earth System Model*. Journal of Advances in Modeling Earth Systems, 11, 4513– 4558. [https://doi.org/10.1029/2019MS001739](https://doi.org/10.1029/2019MS001739)

## Support
* NERC users requiring assistance running this suite on NERC machines (ARCHER, NEXCS, Monsoon) should raise a ticket on the [NCAS-CMS helpdesk](https://cms-helpdesk.ncas.ac.uk).
* Users running this suite on other machines should contact local support services.

