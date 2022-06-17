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

[Fully coupled configurations of UKESM1.1](/_unified-model/configurations/ukesm/relnotes-1.1/coupled) are also available.

## Model and Suite Specifications

The current version of UKESM1.1 has an atmospheric resolution of N96 (~140 km) and a one degree resolution in the ocean. The vertical resolution is 85 levels in the atmosphere and 75 levels in the ocean.

Each configuration of the model is distributed and run as a [Rose]({{site.baseurl}}/pages/rose-cylc) suite.

*Note: that links to suites (and to a couple of other pages) require access to the Met Office Science Repository Service (MOSRS) - see the [introduction to UKESM](/_unified-model/configurations/ukesm) for more details.*

| UM Version | AMIP |
| vn12.1 | [u-cj514](https://code.metoffice.gov.uk/trac/roses-u/browser/c/j/5/1/4/trunk) |

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

## Running on other machines
The model may be run on other (i.e. non-Met Office) machines. See the [introduction to UKESM](/unified-model/configurations/ukesm) for more on available resources and how to access them. More specific instructions for suite settings for different machines are given in the following subsections.

### Monsoon2
To run on Monsoon2, the Met Office / NERC collaborative platform:
 * Set **suite conf -> Host Machine -> Site at which model is being run** to `MONSooN`
 * Ensure these options are set to `false`:
   * **suite conf -> Tasks -> Supermeans** (generation of supermeans)
   * **suite conf -> Tasks -> Archive UM wallclock times** (archiving wallclock times)

Output files created by the suite running on Monsoon2 may be archived via the Met Office Operational Storage Environment (MOOSE). The options for requesting this can be found under the **postproc -> Post Processing - common settings** control panel. Set **archive_command** to `Moose`and provide (or check) values for further options in the subpanel **Moose Archiving**. See [below](#archiving-of-duplexed-data) for more on the **Duplex dataset archiving** option.

Note that you must have a MOOSE account before archiving can work - see [below](#support) for help.

#### Optional configuration settings
To aid portability, the suites use site-specific optional configuration settings which override default values for some parameters when **suite conf -> Machine Options -> Site at which model is being run** is set to `MONSooN`. In particular, when running on Monsoon2, the names for ancillaries in 

* **um -> namelist -> Reconfiguration and Ancillary Control -> Configure ancils and initialise dump fields**

are specified in `app/um/opt/rose-app-monsoon.conf`.

### ARCHER2

#### Setup
To run on ARCHER2, the NERC platform, first set **suite conf -> Host Machine -> Site at which model is being run** to `Archer2`.  Then

1. Setting the site to `Archer2` causes other options to appear under **suite conf -> Project Accounting**.  Set appropriate values for:

* **User account for HPC tasks**
* **Account group for HPC tasks**

2. Under **suite conf -> Domain Decomposition -> Atmosphere**, set **Max number of processes/node** to `128`. This value must also be set for the **Max number of process/node** parameter in **suite conf -> Testing -> Processor Decomposition** and **suite conf -> Testing -> OpenMP** if the respective tests have been turned on (see below).

3. Under **suite conf -> Tasks**, set the following to `false`:

* **Archive UM wallclock times**
* **Archive UM output logs**
* **Supermeans**

4. Under **suite conf -> Testing**, set the following to `false`:

* **OpenMP -> Run No OpenMP test**
* **Diagnostics -> Run increment budget test**

#### Archiving model output
Output files created by the suite running on ARCHER2 may be archived to disk. The options for requesting this can be found under the **postproc -> Post Processing - common settings** control panel. First, set **archive_command** to `Archer`. This causes the subpanels **Archer Archiving** and **JASMIN transfer** to appear under **postproc -> Post Processing - common settings**.  

In **Archer Archiving**, specify the location of the archived files on ARCHER2 by providing values for:

* **archive_root_path** (the location on ARCHER2 where the files are to be archived)
* **archive_name** (the name of the archive)

Following archiving, the files may be optionally transferred to a remote machine such as JASMIN. In **JASMIN transfer**, provide values for:

* **remote_host** (the address of the remote machine) 
* **transfer_dir** (the location of the archived files on the remote machine)

and turn on the transferring of the files by setting **suite conf -> Build and Run -> PP Transfer** to `true`.

Note that, before transfer from ARCHER2 to JASMIN can work, some setup of communication between ARCHER2 and JASMIN is required.  To do this, follow the instructions under **Obtaining a JASMIN short-lived credential** on [this page]({{site.baseurl}}/_archer2/pptransfer) (the section on **Suite Changes** on that page can be ignored, since these suites are already set up for transfer).

#### Optional configuration settings
To aid portability, the suites use site-specific optional configuration settings which override default values for some parameters when **suite conf -> Machine Options -> Site at which model is being run** is set to `Archer2`. In particular, when running on ARCHER2, the names for ancillaries in 

* **um -> namelist -> Reconfiguration and Ancillary Control -> Configure ancils and initialise dump fields**

are specified in `app/um/opt/rose-app-archer2.conf`.

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

