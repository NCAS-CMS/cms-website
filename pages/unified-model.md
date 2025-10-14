---
layout: page-fullwidth
title: Unified Model
subheadline: Unified Model
teaser: The Met Office <a href="https://www.metoffice.gov.uk/research/approach/modelling-systems/unified-model">Unified Model</a> (UM) is a numerical model of the atmosphere used for both weather and climate applications.
permalink: /unified-model/
---

## About the UM

The Unified Model is used by the ​[UK Met Office](https://www.metoffice.gov.uk) for operational numerical weather prediction and by the ​[Hadley Centre for Climate Prediction and Research](https://www.metoffice.gov.uk/weather/climate/met-office-hadley-centre/index) to simulate and predict the Earth's climate.

The UM can be used in atmosphere only mode, or coupled to other models including, but not limited to, the [NEMO ocean](https://www.nemo-ocean.eu/) and CICE sea-ice models via the [OASIS coupler](https://oasis.cerfacs.fr/en/home/), [UKCA chemistry and aerosols](https://www.ukca.ac.uk) and the [JULES land-surface model](https://jules.jchmr.org/).  It can also be used in other modes, including Single Column Model (SCM), Aquaplanet & Exoplanet.

## Running the UM

NCAS-CMS installs and maintains supported UM versions, workflow tools and other associated software on the UK national high performance computer, [ARCHER2]({{ 'archer2' | relative_url }}), via the [PUMA2]({{ 'puma2' | relative_url }}) service. All NCAS researchers can use the UM on this service, details of getting accounts can be found [here]({{ 'puma2' | relative_url }}).

The UM is a complex software system; new users should either: 
* attend one of our organized [UM Introduction training]({{ '/services/training' | relative_url }}) courses; or
* complete the [online training](https://ncas-cms.github.io/um-training/).  

This covers all the essential information needed in order to run a UM suite on ARCHER2, including, how to set up your environment, common errors, use of the workflow management software, source code management, etc.

## UM Versions

The UM undergoes significant changes as new scientific enhancements are introduced or new features are added, and so the [Met Office](https://www.metoffice.gov.uk) release new versions approx. 3-4 times a year.  NCAS-CMS only supports a subset of the versions that have been released.

| **ARCHER2**: | 7.3 | 8.4 | 10.7 | 11.x | 12.x | 13.x |
| **Monsoon3**: | | | | | | 13.x |

The UM source code is held in the [Met Office Science Repository Service](https://code.metoffice.gov.uk/doc/um/) (MOSRS), along with documentation relating to new versions, including the UM User Guides.

## UM Configurations

In order to run the model, users need to have access to a set of files that will enable them to run a particular scientific version of the climate model (describing exactly the physical and dynamical choices within the UM system).  NCAS-CMS port certain "standard" configurations to the National HPC system ARCHER2.

See the [UM Configurations](configurations) page for full details on suites that have been ported to ARCHER2.

## JASMIN archiving

CMS have set up the infrastructure for automatic archiving of data from ARCHER2 to JASMIN. To include this in your workflow, follow the instructions below:  

* [Upgrading Postproc for ARCHER2/JASMIN](postproc)
* [Configuring PPTransfer](pptransfer-globus)
* [Adding JASMIN ET data migration to a UM workflow](jdma)
