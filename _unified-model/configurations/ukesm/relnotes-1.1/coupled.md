---
title: UKESM1.1-coupled Release Notes
teaser: Release notes for the fully coupled configurations of version 1.1 of the UK Earth System Model (UKESM).
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

An [atmosphere-only (AMIP) configuration of UKESM1.1](/_unified-model/configurations/ukesm/relnotes-1.1/amip.md) is also available for use.

## Model and suite specifications
The current version of UKESM1.1 has an atmospheric resolution of N96 (~140 km) and a one degree resolution in the ocean. The vertical resolution is 85 levels in the atmosphere and 75 levels in the ocean.

Each configuration of the model is distributed and run as a [Rose]({{site.baseurl}}/pages/rose-cylc) suite.

*Note that links to suites (and to a couple of other pages) require access to the Met Office Science Repository Service (MOSRS) - see the [introduction to UKESM](/_unified-model/configurations/ukesm.md) for more details.*

### historical, pre-industrial control
There are two fully coupled UKESM1.1 configurations which each make use of all model components: one with science settings for a historical experiment, and one with settings for a pre-industrial control experiment.

| UM version | historical | pre-industrial control |
| vn12.1 | [u-cj512](https://code.metoffice.gov.uk/trac/roses-u/browser/c/j/5/1/2/trunk) | [u-cj511](https://code.metoffice.gov.uk/trac/roses-u/browser/c/j/5/1/1/trunk) |

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

### abrupt4xCO2, 1%CO2
Configurations for abrupt4xCO2 and 1%CO2 experiments can be created using the pre-industrial control experiment as a starting point.

To create a suite for the abrupt4xCO2 experiment, first make a copy of the [pre-industrial control suite](https://code.metoffice.gov.uk/trac/roses-u/browser/c/j/5/1/1/trunk), then in **um -> namelist -> UM Science Settings -> Section 01-02 - Radation -> GAS MMRs**, set `co2_mmr=1.72728e-03`.

To create a suite for the 1xCO2 experiment, first make a copy of the [pre-industrial control suite](https://code.metoffice.gov.uk/trac/roses-u/browser/c/j/5/1/1/trunk), then in **um -> namelist -> UM Science Settings -> Section 01-02 - Radation -> GAS MMRs -> Varying gas MMRs**, set `l_clmchfcg=.true.` to enable time-varying GHGs. Finally, in the sub-panel **Varying CO2 MMRs**, set
~~~
clim_fcg_levls_co2=4.3182e-04
clim_fcg_nyears_co2=1
clim_fcg_rates_co2=1.0
clim_fcg_years_co2=1849
~~~
See [below](#science-notes) for more on the science settings of the model.

## Running on the Met Office HPC
By default, each UKESM1.1 suite is set up to run the model on the Met Office HPC (i.e. **suite conf -> Machine Options -> Site at which model is being run** is set to `MetO Cray`). The suite offers several options for specifying how the model is to be run, including:

* login node to be used for submission to Met Office HPC: **suite conf -> Machine Options -> MetO Cray login node**
* Met Office queue to which jobs will be submitted: **suite conf -> Machine Options -> HPC queue**

Options for specifying the account under which jobs will be run are available in **suite conf -> Project Accounting**:

* Select **Use default account** to use the default account for your department.
* If this is set to `false`, then choose an option from the **Account** menu.
* If the option is `other`, then enter the account explicitly in **'Other' user account**.

## Running on other machines
The model may be run on other (i.e. non-Met Office) machines. See the [introduction to UKESM1](/_unified-model/configurations/ukesm) for more on available resources and how to access them. More specific instructions for suite settings for different machines are given in the following subsections.

### Monsoon2
To run on Monsoon2, the Met Office / NERC collaborative platform, set **suite conf -> Machine Options -> Site at which model is being run** to `MONSooN`.

Output files created by the suite running on Monsoon2 may be archived via the Met Office Operational Storage Environment (MOOSE). The options for requesting this can be found under the **postproc -> Post Processing - common settings** control panel. Set **archive_command** to `Moose` and provide (or check) values for further options in the subpanel **Moose Archiving**. See [below](#archiving-of-duplexed-data) for more on the `non_duplexed_set` option.

Note that you must have a MOOSE account before archiving will work - see [below](#support) for help.

### ARCHER2

#### Setup
To run on ARCHER2, the NERC platform, first set **suite conf -> Machine Options -> Site at which model is being run** to `Archer2` and then:

1. Set these other **Machine Options**:

* **Use Environment Modules** to `Custom module files`
* **Science Configuration Module Name** to `GC3-PrgEnv/2.0/2021.12.15`
* **Module file location** to `/work/y07/shared/umshared/moci/modules/modules`

2. Setting the site to `Archer2` causes other options to appear under **suite conf -> Project Accounting**.  Set appropriate values for:

* **User account for HPC tasks**
* **Account group for HPC tasks**

3.  Under **suite conf -> Domain Decomposition -> Atmosphere**, set:

* **Use max processes per node** to `false`
* **Max number of processes/node** to `128`

4.  Under **suite conf -> Testing**, set the following to `false`:

* **Test restartability**
* **Test rigorous compiler option**
* **Test PE decomposition change**
* **Archive integrity**
* **CPMIP Analysis -> CPMIP load balancing analysis**

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
To aid portability, the suites use site-specific optional configuration settings which override default values for some parameters when **suite conf -> Machine Options -> Site at which model is being run** is set to `Archer2`. In particular, when running on ARCHER2, the file names for the following 

* **um -> namelist -> Reconfiguration and Ancillary Control -> General technical options -> ainitial**
* **nemo_cice -> Restart files -> NEMO restart file**
* **nemo_cice -> Restart files -> NEMO iceberg restart file**
* **nemo_cice -> Restart files -> CICE restart file**
* **ocean_passive_tracers -> env -> Initialisaton Settings -> Restart file to initialize (CFC-Age)**
* **ocean_passive_tracers -> env -> Initialisaton Settings -> Passive tracers restart file**

are specified in `opt` files - specifically:

* `app/um/opt/rose-app-archer2.conf`
* `app/nemo_cice/opt/rose-app-archer2.conf`
* `app/um/ocean_passive_tracers/rose-app-archer2.conf`

## Archiving of duplexed data
When running on Met Office machines (including Monsoon2), the suite will, by default, archive a single copy of its data to MOOSE. For critical model runs, this setting may be changed to archive two copies of the data (i.e. duplex) by switching `non_duplexed_set` in **postproc -> Post Processing-common settings -> Moose Archiving** to `false`. Further guidance on when to choose this option is available at [MassNonDuplexPolicy](http://www-twiki/Main/MassNonDuplexPolicy) (note that this link only works from within the Met Office).

## Compute Resource Usage
The compute resources used by the suite can be set via parameters on the **suite conf -> Machine Options** and **suite conf -> Domain Decomposition** control panels. The following discussion is specific to the Met Office HPC for the most part, but may still be helpful for users of other machines.

The type of compute node can be set via **suite conf -> Machine Options -> XC40 core type**: a `Haswell` node has 32 cores, while `Broadwell` has 36.

The suite is currently set up in **suite conf -> Domain Decomposition** to use 36 nodes (see [below](#calculation-of-node-count) for more details on how this is calculated). An alternative setup uses 19 nodes. Parameter settings for both setups are:

|Parameter |	36 node suite | 19 node suite |
| -------- | ------------- | ------------- |
| Atmosphere: Processes East-West	 | 32 | 32 |
| Atmosphere: Processes North-South | 18 | 18 |
| IO Server Processes | 0| 0 |
| OpenMP threads for the atmosphere | 2 | 1 |
| NEMO: Number of processes East-West | 12 | 9 |
| NEMO: Number of processes North-South | 9 | 8 |
| NEMO: Number of processes in XIOS server | 6 |6 |
| OpenMP threads for the ocean | 1 |1 |

Note that the ocean must be rebuilt (by setting **suite conf -> Build and Run -> Build Ocean** to `true`) whenever the NEMO parameters in the table are changed during a run.

Setting these parameters to other values may require load balancing to ensure that HPC resources are being used in the most efficient fashion.

## Calculation of node count
On **suite conf -> Domain Decomposition -> Atmosphere**, the number of processes used by the UM can be set via **Atmosphere: Processes East-West** and **Atmosphere: Processes North-South**; additional processes for the IO Server may be requested using **IO Server Processes**. Finally, **OpenMP threads for the atmosphere** sets the number of threads for each process; multiplying this by the number of processes gives the number of compute tasks.

Using the parameter values for the 36 node suite, the number of tasks used by the UM is `(32 * 18 + 0) * 2 = 1152`. Dividing by the number of cores per node (in this case `36`) and rounding up (because different executables cannot run on the same node) gives 32 compute nodes used by the atmosphere.

A similar calculation may be performed for the settings on **suite conf -> Domain Decomposition -> Ocean**; using **NEMO: Number of processes East-West**, **NEMO: Number of processes North-South** and **OpenMP threads** for the ocean to give `12 * 9 * 1 = 108` tasks, or 3 compute nodes used by the ocean.

Finally, on the same control panel, **NEMO: Number of processes in XIOS server** is set to `6`, which equates to 1 compute node used by XIOS.

Thus, the total number of nodes used by the suite is `32 + 3 + 1 = 36`.

## Tests in the suite
The suite contains options for testing different aspects of the model including reproducible restarting, changes in processor decomposition, comparison to known good output and integrity of archived files. Some of these tests may be of more interest to developers than general users of the model; they can be turned on or off via the **suite conf -> Testing** control panel.

### Testing for PE decomposition change
Changing the PE decomposition will change the results of the model because of the behaviour of the chemistry solver within the UM. Thus, by default, the Test PE decomposition change test (see **suite conf -> Testing**) will fail, and so this test has been turned off. There is a version of the chemistry solver which does not change results; this can be selected by setting **um -> namelist -> UM Science Settings -> Section 34 - UKCA: UK Aerosols and chemistry -> Chemistry -> l_ukca_asad_columns** to `true`. With this option selected, the PE decomposition change test should pass.

Note that we do not select this version of the chemistry solver by default because it has a performance overhead; specifically, it causes an atmosphere-only job to run about 10% slower than when running with option turned off.

It should be noted that changing the PE decomposition for the ocean in UKESM will also change results because this changes results for both the iceberg code in NEMO and for the CICE code. This behaviour cannot be rectified by setting a single variable (that is, there is no analogue of **l_ukca_asad_columns** for NEMO and CICE).

## Known issues
* Development work on the UKESM1.1 um12.1 coupled configurations (including instructions on how to upgrade suites, where necessary) is documented in  [ticket #830](https://code.metoffice.gov.uk/trac/UKESM/ticket/830) on MOSRS.

## Support
* NERC users requiring assistance running this suite on NERC machines (ARCHER2 & Monsoon) should raise a ticket on the [NCAS-CMS helpdesk](https://cms-helpdesk.ncas.ac.uk).
* Users running this suite on other machines should contact local support services.
