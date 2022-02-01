---
title: UKESM1-AMIP Release Notes
teaser: Release notes for the atmosphere-only (AMIP) configuration of the UK Earth System Model (UKESM1).  
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

[Fully coupled configurations of UKESM1](/cms-website/unified-model/configurations/ukesm/relnotes-1.0/coupled) are also available.

## Model and Suite Specifications

The current version of UKESM1 has an atmospheric resolution of N96 (~140 km) and a one degree resolution in the ocean. The vertical resolution is 85 levels in the atmosphere and 75 levels in the ocean.

Each configuration of the model is distributed and run as a [Rose](#TODO) suite.

*Note: that links to suites (and to a couple of other pages) require access to the Met Office Science Repository Service (MOSRS) - see the [introduction to UKESM1](/cms-website/unified-model/configurations/ukesm) for more details.*

| UM Version | AMIP |
| vn11.1 | [u-be303](https://code.metoffice.gov.uk/trac/roses-u/browser/b/e/3/0/3/trunk) |

See [below](#science-notes) for more on the science settings of the AMIP configuration, and its relationship to the fully coupled configurations of UKESM1.

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

## Running on the Met Office HPC
By default, each UKESM1 suite is set up to run the model on the Met Office HPC (i.e. *"suite conf -> Host Machine -> Site at which model is being run"* is set to **MetO Cray ('meto_cray')**).

The suite offers several further options for specifying how the model is to be run, including:

* login node to be used for submission to Met Office HPC: *"suite conf -> Host Machine -> Compute Host"*
* Met Office queue to which jobs will be submitted: *"suite conf -> Host Machine -> HPC queue"*

Options for specifying the account under which jobs will be run are also available in *"suite conf -> Host Machine"*:

* Select **Use default account** to use the default account for your department.
* If this is set to `false`, then choose an option from the **Account** menu.
* If the option is `other`, then enter the account explicitly in **'Other' user account**.

## Running on other machines
The model may be run on other (i.e. non-Met Office) machines. See the [introduction to UKESM1](/cms-website/unified-model/configurations/ukesm) for more on available resources and how to access them. More specific instructions for suite settings for different machines are given in the following subsections.

### Monsoon
To run on Monsoon, the Met Office / NERC collaborative platform:
 * Set *"suite conf -> Host Machine -> Site at which model is being run"* to **MONSooN ('monsoon')**
 * Ensure the generation of supermeans (see *"suite conf -> Tasks -> Supermeans"*) is turned off

Output files created by the suite running on Monsoon may be archived via the Met Office Operational Storage Environment (MOOSE). The options for requesting this can be found under the *"postproc -> Post Processing - common settings"* control panel. Set `archive_command` to **Moose** and provide (or check) values for further options in the subpanel *"Moose Archiving"*. See [below](#TODO) for more on the `non_duplexed_set` option.

Note that you must have a MOOSE account before archiving can work - see [below](#TODO) for help.

### ARCHER2

{% include alert warning="Rewrite for ARCHER2 - user u-be303/archer2" %}

To run on Archer, the NERC platform, set *"suite conf -> Host Machine -> Site at which model is being run"* to Archer.

When running on Archer, the maximum number of processes per node (see suite conf -> Domain Decomposition -> Atmosphere -> Max number of processes/node) must be set to 24. This value must also be set for the Max number of process/node parameter in suite conf -> Testing -> Processor Decomposition and suite conf -> Testing -> OpenMP if the respective tests have been turned on (see below).

In addition, the following options (see below) must be turned off when running on Archer:

suite conf -> Tasks -> Archive UM wallclock times
suite conf -> Tasks -> Archive UM output logs
suite conf -> Tasks -> Supermeans
suite conf -> Testing -> OpenMP -> Run No OpenMP test
suite conf -> Testing -> Diagnostics -> Run increment budget test
Output files created by the suite running on Archer may be archived to disk. The options for requesting this can be found under the postproc -> Post Processing - common settings control panel. Set archive_command to Archer and provide values for archive_root_path and archive_name in the subpanel Archer Archiving to specify the location of the archived files on Archer.

Following archiving, the files may be optionally transferred to a remote machine such as JASMIN. Provide values for remote_host (the address of the remote machine) and transfer_dir (the location of the archived files on the remote machine) in the subpanel JASMIN Transfer. In addition, transferring must be turned on by setting suite conf -> Tasks -> PP Transfer to true.

Note that, before transfer from Archer to JASMIN can work, some setup of communications (specifically, both between PUMA and Archer data transfer node?, and between Archer data transfer node and JASMIN?) is required.

## Using the model in a CMIP6 production run
Using the model in a CMIP6 production run requires the provision of extra information (for example, the MIP and the experiment to which the run is contributing). This information must be specified in the suite, and the suite will check its validity. See ​[here on the MOSRS](https://code.metoffice.gov.uk/trac/ukcmip6/wiki/ExperimentGuidance) for more details about this information.

By default, the suite is not set up to run in full CMIP6 production mode, so this information is not required. To change this, set *"suite info -> project"* to `u-cmip6` (which will expose the interface in suite info for collecting this information). More information on setting up a CMIP6 experiment is available ​on [MOSRS](https://code.metoffice.gov.uk/trac/ukcmip6/wiki/ExperimentGuidance).

## Archiving of duplexed data
When running on Met Office machines (including Monsoon), the suite will, by default, archive a single copy of its data to MOOSE. For critical model runs, this setting may be changed to archive two copies of the data (i.e. duplex) by turning on **Duplex dataset archiving** in *"suite conf -> Host Machine"*. Further guidance on when to choose this option is available at ​[MASSNonDuplexPolicy](http://www-twiki/Main/MassNonDuplexPolicy) (Note that this link only works from within the Met Office).

## Tests in the suite
The suite contains options for testing different aspects of the model including reproducible restarting, changes in processor decomposition, comparison to known good output (KGO) and integrity of archived files. Some of these tests may be of more interest to developers than general users of the model; they can be turned on or off via the *"suite conf -> Testing"* control panel.

## Science notes
UKESM1-AMIP is an atmosphere-only version of the fully coupled UKESM1 configuration and for CMIP6 is run for the period 1979-2014. Its design follows the experiment design of ​[Eyring et al (2016)](https://gmd.copernicus.org/articles/9/1937/2016/). The following Earth System components are not included in the AMIP:

* Ocean and sea ice models (NEMO/CICE)
* Interactive ocean biogeochemistry model (MEDUSA)
* Land carbon cycle and dynamic vegetation model (TRIFFID)

Instead, the AMIP configuration uses observed sea surface temperatures and sea ice concentrations ​[as provided by PCMDI](https://pcmdi.llnl.gov/mips/amip/). Vegetation (vegetation fractions, Leaf Area Index, canopy height) and surface ocean biology fields (DMS and chlorophyll) required as inputs to the model atmosphere are prescribed from member `r5i1p1f3` of the UKESM1 CMIP6 historical ensemble, thereby maintaining traceability to the fully coupled model. Vegetation is therefore not dynamic (i.e. it is not predicted in the AMIP model) but the prescribed vegetation and its characteristics mirror those simulated by the TRIFFID dynamic vegetation scheme in the coupled historical run, as is the case for the surface ocean biological fields.

Some additional detail about the prescribed fields:

* prescribed vegetation fractions are a transient annual mean from the historical run. This allows time-varying land use change to be included in the AMIP run in a manner consistent with its treatment in the coupled historical simulations.
* prescribed LAI is a 1979-2014 multi-annual monthly climatology of the historical run.
* prescribed canopy height is a 1979-2014 annual mean climatology of the historical run.
* prescribed ocean DMS and chlorophyll concentrations are a 1979-2014 multi-annual monthly climatology of the historical run.

## Known issues
* The UKESM1 AMIP suite uses a prescribed climatology of vegetation properties; vegetation fractions, leaf area index (LAI) and canopy height. These climatologies were constructed from data from the UKESM1 historical simulations, but the seasonal cycle of LAI was found to be incorrect and is six months out of phase. This error has been corrected with a new LAI climatology file at [​revision 147944 of the suite](https://code.metoffice.gov.uk/trac/roses-u/browser/b/e/3/0/3/trunk?rev=147944). Working copies of the suite should be updated to use this revision.

* All Stash items spanning `38:485` to `38:545`: `Aerosol surface conc., concn., load diagnostics`: Due to the way STASH is handling and processing these items, they will be output as exactly **1/3rd of their actual value**. The values of these items must therefore be scaled by a factor of 3.0.

* Development work on the AMIP suite (including instructions on how to upgrade suites, where necessary) is documented on  MOSRS in [ticket #657](https://code.metoffice.gov.uk/trac/UKESM/ticket/657).

## Support
* NERC users requiring assistance running this suite on NERC machines (ARCHER2 & Monsoon) should raise a ticket on the [NCAS-CMS helpdesk](https://cms-helpdesk.ncas.ac.uk).
* Users running this suite on other machines should contact local support services.

