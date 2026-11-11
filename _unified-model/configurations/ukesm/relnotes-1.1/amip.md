---
title: UKESM1.1-AMIP Release Notes
teaser: Release notes for the atmosphere-only (AMIP) configuration of version 1.1 of the UK Earth System Model (UKESM).  
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

[Fully coupled configurations of UKESM1.1](/unified-model/configurations/ukesm/relnotes-1.1/coupled) are also available.

## Model and Suite Specifications

The current version of UKESM1.1 has an atmospheric resolution of N96 (~140 km) and a one degree resolution in the ocean. The vertical resolution is 85 levels in the atmosphere and 75 levels in the ocean.

Each configuration of the model is distributed and run as a [Rose]({{site.baseurl}}/rose-cylc) suite.

*Note: that links to suites (and to a couple of other pages) require access to the Met Office Science Repository Service (MOSRS) - see the [introduction to UKESM](/unified-model/configurations/ukesm) for more details.*

UKESM workflows suitable for use (as of August 2026) can be found [here](https://code.metoffice.gov.uk/trac/UKESM/wiki/UKESM1.1StandardJobs).

See [below](#science-notes) for more on the science settings of the AMIP configuration, and its relationship to the fully coupled configurations of UKESM1.1.

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

## Running on the Met Office HPC
By default, each UKESM1.1 suite is set up to run the model on the Met Office HPC (i.e. **suite conf -> Host Machine -> Site at which model is being run** is set to `MetO Cray`). The suite offers several further options for specifying how the model is to be run, including:

* login node to be used for submission to Met Office HPC: **suite conf -> Host Machine -> Compute Host**
* Met Office queue to which jobs will be submitted: **suite conf -> Host Machine -> HPC queue**

Options for specifying the account under which jobs will be run are also available in **suite conf -> Host Machine**:

* Select **Use default account** to use the default account for your department.
* If this is set to `false`, then choose an option from the **Account** menu.
* If the option is `other`, then enter the account explicitly in **'Other' user account**.


## Archiving of duplexed data
When running on Met Office machines (including Monsoon2), the suite will, by default, archive a single copy of its data to MOOSE. For critical model runs, this setting may be changed to archive two copies of the data (i.e. duplex) by setting **Duplex dataset archiving** in **suite conf -> Host Machine** to `true`. Further guidance on when to choose this option is available at [MassNonDuplexPolicy](http://www-twiki/Main/MassNonDuplexPolicy) (note that this link only works from within the Met Office).

## Tests in the suite
The suite contains options for testing different aspects of the model including reproducible restarting, changes in processor decomposition, comparison to known good output (KGO) and integrity of archived files. Some of these tests may be of more interest to developers than general users of the model; they can be turned on or off via the **suite conf -> Testing** control panel.

## Science notes
UKESM1.1-AMIP is an atmosphere-only version of the fully coupled UKESM1.1 configuration and for CMIP6 is run for the period 1979-2014. Its design follows the experiment design of [Eyring et al (2016)](https://gmd.copernicus.org/articles/9/1937/2016/). The following Earth System components are not included in the AMIP:

* Ocean and sea ice models (NEMO/CICE)
* Interactive ocean biogeochemistry model (MEDUSA)
* Land carbon cycle and dynamic vegetation model (TRIFFID)

Instead, the AMIP configuration uses observed sea surface temperatures and sea ice concentrations [as provided by PCMDI](https://pcmdi.llnl.gov/mips/amip/). Vegetation (vegetation fractions, Leaf Area Index, canopy height) and surface ocean biology fields (DMS and chlorophyll) required as inputs to the model atmosphere are prescribed from member `r5i1p1f3` of the UKESM1 CMIP6 historical ensemble, thereby maintaining traceability to the fully coupled model. Vegetation is therefore not dynamic (i.e. it is not predicted in the AMIP model) but the prescribed vegetation and its characteristics mirror those simulated by the TRIFFID dynamic vegetation scheme in the coupled historical run, as is the case for the surface ocean biological fields.

Some additional detail about the prescribed fields:

* prescribed vegetation fractions are a transient annual mean from the historical run. This allows time-varying land use change to be included in the AMIP run in a manner consistent with its treatment in the coupled historical simulations.
* prescribed LAI is a 1979-2014 multi-annual monthly climatology of the historical run.
* prescribed canopy height is a 1979-2014 annual mean climatology of the historical run.
* prescribed ocean DMS and chlorophyll concentrations are a 1979-2014 multi-annual monthly climatology of the historical run.

## Known issues
* Development work on the UKESM1.1 um12.1 configurations (including instructions on how to upgrade suites, where necessary) is documented in [ticket #830](https://code.metoffice.gov.uk/trac/UKESM/ticket/830) on MOSRS.

## Support
* NERC users requiring assistance running this suite on NERC machines (ARCHER2 & Monsoon2) should raise a ticket on the [NCAS-CMS helpdesk](https://cms-helpdesk.ncas.ac.uk).
* Users running this suite on other machines should contact local support services.

