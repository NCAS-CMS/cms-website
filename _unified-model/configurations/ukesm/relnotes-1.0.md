---
title: UKESM1 Release Notes
---
These are the notes for the first release of the UK Earth System Model (UKESM1). Some background information on the model, its components and the prerequisites for using it can be found in the [introduction to UKESM1](/unified-model/configurations/ukesm/).

## Model Configurations

The model is available in a number of configurations for running different types of experiment:

* [Atmosphere-only](amip):
The so-called **AMIP** configuration, in which the model atmosphere is forced by observed sea surface temperature and sea ice boundary conditions.

* [Coupled](coupled)::
Two fully coupled configurations, which each make use of all model components:
  * one set up to run the CMIP6 **pre-industrial** control experiment, and
  * one to run the CMIP6 **historical** experiment.

There are also additional coupled configurations for the CMIP6 **abrupt4xCO2** and **1%CO2** experiments, which can be created using the pre-industrial control experiment as a starting point.

A full description of how to access and run each configuration can be found on the [AMIP](relnotes-1-0-amip) and [Coupled](relnotes-1-0-coupled) configuration pages.

## Support
* NERC users requiring assistance running this suite on NERC machines (ARCHER, NEXCS, Monsoon) should raise a ticket on the [NCAS-CMS helpdesk](https://cms-helpdesk.ncas.ac.uk).
* Users running this suite on other machines should contact local support services.

