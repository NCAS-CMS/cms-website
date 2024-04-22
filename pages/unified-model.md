---
layout: page-fullwidth
title: Unified Model
subheadline: Unified Model
teaser: The Met Office <a href="https://www.metoffice.gov.uk/research/approach/modelling-systems/unified-model">Unified Model</a> (UM) is a numerical model of the atmosphere used for both weather and climate applications.
permalink: /unified-model/
---
<div class="row">
<div class="medium-4 medium-push-8 columns" markdown="1">
<div class="panel radius" markdown="1">
**Table of Contents**
{: #toc }
*  TOC
{:toc}
</div><!-- /.panel -->
</div><!-- /.medium-4 -->

<div class="medium-8 medium-pull-4 columns" markdown="1">

The Unified Model is used by the ​[UK Met Office](https://www.metoffice.gov.uk) for operational numerical weather prediction and by the ​[Hadley Centre for Climate Prediction and Research](https://www.metoffice.gov.uk/weather/climate/met-office-hadley-centre/index) to simulate and predict the Earth's climate.

The UM can be used in atmosphere only mode, or coupled to other models including, but not limited to, the [NEMO ocean](https://www.nemo-ocean.eu/) and CICE sea-ice models via the [OASIS coupler](https://portal.enes.org/oasis), [UKCA chemistry and aerosols](https://www.ukca.ac.uk) and the [JULES land-surface model](https://jules.jchmr.org/).  It can also be used in other modes, including Single Column Model (SCM), Aquaplanet & Exoplanet.

## Running the UM
The UM is a complex software system; new users should either attend one of our organized [UM Introduction training]({{ '/services/training' | relative_url }}) courses or complete the [online training](https://ncas-cms.github.io/um-training/).  This covers all the essential information needed in order to run a UM suite on the national HPC service; ARCHER2, including, how to set up your environment, common errors, use of the workflow management software, source code management, etc.

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->
NCAS-CMS installs and maintains the supported UM versions, workflow tools and other associated software on the UK national high performance computer. All NCAS researchers can use the UM on this service, details of getting accounts can be found here.

## UM Versions

The UM undergoes significant changes as new scientific enhancements are introduced or new features are added, and so the [Met Office](https://www.metoffice.gov.uk) release new versions approx. 3-4 times a year.  NCAS-CMS only supports a subset of the versions that have been released.

| **ARCHER2**: | 7.3 | 8.4 | 10.7 | 11.x | 12.x |
| **Monsoon2**: | 10.x | 11.x | 12.x |

Documentation relating to new UM versions, including the UM User Guides, is available on the [Met Office Science Repository Service](https://code.metoffice.gov.uk/doc/um/) (MOSRS).

## UM Configurations

### Climate Configurations

In order to run the climate model, users need to have access to a set of files that will enable them to run a particular scientific version of the climate model (describing exactly the physical and dynamical choices within the UM system).  NCAS-CMS port certain "standard" configurations to the National HPC system ARCHER2, including the HadGEM3 model family.

See the [UM Configurations](configurations) page for full details on suites that have been ported to ARCHER2 and Monsoon2.

### Nesting Suite Configurations

Nested limited area models can easily be set up using the Met Office ​[Nesting Suite](https://code.metoffice.gov.uk/trac/rmed/wiki/suites/nesting). These are Rose suites and can be run on ARCHER2 and Monsoon2, allowing scientists to define up to five nested domains, a choice of science configurations and easy ancillary file generation for the chosen domains. 

| ARCHER2 suite id | Owner | Met Office original suite id | UM Version | Description |
| :----: | :----: | :----: | :----: | ---- |
| u-ca103 | grenvillelister | u-av356 | 11.1 | Nesting Suite for RA2 - February 2018 |
| u-by395/archer2 | claudiosanchez| u-by395 | 11.7 | Nesting Suite for RA3+ |

## UM Documentation

* [Configuring PPTransfer](pptransfer)
* [How to add JASMIN ET data migration to UM Workflow](jdma)
* [How to add Ozone Redistribution to a GC3.1 suite](ozone-redistribution)

## Single Column Model

The [Single Column Model](single-column-model) page explains how to run the Met Office Single Column model on various computers.

## Source Code Browsers

The UM Fortran source code is available to view via MOSRS [UM Repository](https://code.metoffice.gov.uk/trac/um/) or alternatively has been converted into a hyperlinked website hosted on PUMA.  See [UM Source Code Browsers](code-browsers).
