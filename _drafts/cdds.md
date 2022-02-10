---
layout: page-fullwidth
title: CDDS
teaser: CMIP6 data CMOR'isation - How to run CDDS workflow on JASMIN
---

### 1. JASMIN GWS Access

You will need access to `cmip6_prep` group workspace.  You can apply for this on the [JASMIN accounts portal](https://accounts.jasmin.ac.uk/services/group_workspaces/cmip6_prep/).

### 2. MOSRS Access

You will need MOSRS access from JASMIN. See [Authentication Caching](https://code.metoffice.gov.uk/trac/home/wiki/AuthenticationCaching) on MOSRS for how to set this up.

### 3. Where to run CDDS

The CDDS work flow comprises several phases:

* preparation
* data reformatting
* quality check

The preparation phase runs interactively, is light on computational resource and can be run on `jasmin-cylc`. Data reformatting is computationally intensive, runs on LOTUS, and is monitored from `jasmin-cylc`. The quality check runs interactively but **SHOULD NOT** be run on `jasmin-cylc` - one of the `jasmin-sci` machines will be appropriate.

*Note: CDDS sources its own bespoke environment. To avoid potential conflicts, your environment should be as simple as possible - you may need to alter it to allow CDDS to run*

### 4. Model Data

CDDS expects data to be in a JASMIN group workspace. CDDS supports two data directory structures:

  1. Data by stream - data from MASS will be structured by stream (ap4, ap5, apm…)
  2. Data by cycle - data from ARCHER2 (and possibly Monsoon2) will be structured by cylc cycle (18500101T0000Z, 18500111T0000Z, 18500401T0000Z, …)

### 5. Running CDDS

The CDDS work flow is driven by the *json request file*. This holds information about the MIP, the experiment, streams to be processed, start and end dates, the source model suite id, and more.

Where possible you should generate the json request file. You will need access to Met Office internal systems to do that. However, it might not be difficult to modify an existing request file for your use; you will need knowledge of the MIP and the experiment for this. An example file is shown [below](TODO).

#### Ocean data preparation
Several NEMO data sets need to be pre-processed to remove halos prior to CDDS processing. CMS have developed a Rose suite (`u-bn582`) to automate halo removal; see [documentation for CDDS-Halo](http://cms.ncas.ac.uk/wiki/CDDS/halo). The suite is available from the MOSRS suite repository. We suggest creating a fully halo-removed dataset prior to running CDDS.

#### Example conversion process
There follows an example work flow, illustrative of the CDDS process. The example is specific to AerChemMIP for experiment piClim-NTCF (see ​https://rawgit.com/WCRP-CMIP/CMIP6_CVs/master/src/CMIP6_experiment_id.html and ​https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_experiment_id.json for information about individual experiments).

1. In your GWS, create a top-level directory for the experiment - this will later become synonymous with `$CDDS_DIR` (I chose to name it `AerChemMIP-piClim-NTCF` in this case).

2. Change directory to `AerChemMIP-piClim-NTCF` - all work should take place here

  `cd AerChemMIP-piClim-NTCF`
  
3. Copy the conversion process orchestration script `cdds_workflow_for_user.sh` to this directory:
 
  **cdds v1.3.2**

  `wget https://raw.githubusercontent.com/NCAS-CMS/NCAS-Useful-Documentation/master/cdds_operationl_scripts/cdds_workflow_for_user_v132.sh`
  `mv cdds_workflow_for_user_v132.sh cdds_workflow_for_user.sh`
  
  **cdds v1.3.3**

  `wget https://raw.githubusercontent.com/NCAS-CMS/NCAS-Useful-Documentation/master/cdds_operationl_scripts/cdds_workflow_for_user_v133.sh`
  `mv cdds_workflow_for_user_v133.sh cdds_workflow_for_user.sh`

  Take a look at the script - it's not complicated.

4. Edit `cdds_workflow_for_user.sh` to set the environment variables `CDDS_DIR`, `REQUEST_JSON` and `FILEPATHSTYPE`
~~~
  export CDDS_DIR="<full-path>/AerChemMIP-piClim-NTCF"
  REQUEST_JSON=AerChemMIP-piClim-NTCF-req.json
  export FILEPATHSTYPE="ARCHER"
~~~

  *Note: call the `REQUEST_JSON` file something memorable - there may be several in your workflow.*

  Note on `FILEPATHSTYPE`
  * for MASS-type data (e.g. `$SUITE/STREAM/files`) use `FILEPATHSTYPE="METOFFICE"`
  * for Archer-type data (e.g. `$SUITE/YYYYMMDDT0001Z/files`) use `FILEPATHSTYPE="ARCHER"`
  * for data retrieved from MASS to Jasmin, the file structure will be `$SUITE/STREAM.pp/files` - you will have to change the names of the `STREAM.pp` dirs to `STREAM` and use `FILEPATHSTYPE="ARCHER"` since this way the dir structure will comply with the Archer-type paths. We DO NOT support any other type of input data directory structure.

**NOTE for running individual steps of CDDS on Jasmin:**
If you need to run individual steps of the pipeline (e.g. `cdds_convert` once you are on `jasmin-cylc` or `cdds_extract` for some testing) outside the regular workflow, you will still have to place all the system and run variables in your environment. For this purpose you can take the ready made file at ​https://raw.githubusercontent.com/cedadev/jasmin-cdds/master/operational_scripts/setup_environment.sh?token=AG5EFI5GAXTKMG7C4KOYKN26QTEAG and either copy paste or download the file, edit the user defined variables at the top, source it and you are ready to run each of the cdds steps individually.

5. Create the json request file, naming the same as `$REQUEST_JSON` set in point 4 above -- here's the one used in our example. Much of the information listed here is taken directly from the `rose-suite.info` file for the UM model suite that generated the data (`u-bh543` for our example) - REMEMBER to consult ​https://rawgit.com/WCRP-CMIP/CMIP6_CVs/master/src/CMIP6_experiment_id.html and ​https://github.com/WCRP-CMIP/CMIP6_CVs/blob/master/CMIP6_experiment_id.json for information about individual experiments, specifically how to set your `parent_experiment_id` variable in the json file!!

~~~
{
  "atmos_timestep": 1200,
  "branch_date_in_child": "1850-01-01-00-00-00",
  "branch_date_in_parent": "1850-01-01-00-00-00",
  "branch_method": "standard",
  "calendar": "360_day",
  "child_base_date": "1850-01-01-00-00-00",
  "config_version": "1.0.5",
  "experiment_id": "piClim-NTCF",
  "parent_experiment_id": "piControl",
  "institution_id": "MOHC",
  "license": "CMIP6 model data produced by the Met Office Hadley Centre is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License (https://creativecommons.org/licenses). Consult https://pcmdi.llnl.gov/CMIP6/TermsOfUse for terms of use governing CMIP6 output, including citation requirements and proper acknowledgement. Further information about this data, including some limitations, can be found via the further_info_url (recorded as a global attribute in this file) and at https://ukesm.ac.uk/cmip6. The data producers and data providers make no warranty, either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose. All liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest extent permitted by law.\n\n ",
  "mip": "AerChemMIP",
  "mip_era": "CMIP6",
  "model_id": "UKESM1-0-LL",
  "model_type": "AGCM AER CHEM",
  "package": "round-1-monthly",
  "parent_base_date": "1850-01-01-00-00-00",
  "parent_mip": "CMIP",
  "parent_mip_era": "CMIP6",
  "parent_model_id": "UKESM1-0-LL",
  "parent_time_units": "days since 1850-01-01-00-00-00",
  "parent_variant_label": "r1i1p1f2",
  "request_id": "UKESM1-0-LL_piClim-NTCF_r1i1p1f2",
  "run_bounds": "1850-01-01-00-00-00 1895-01-01-00-00-00",
  "run_bounds_for_stream_ap4": "1850-01-01-00-00-00 1895-01-01-00-00-00",
  "run_bounds_for_stream_ap5": "1850-01-01-00-00-00 1895-01-01-00-00-00",
  "sub_experiment_id": "none",
  "suite_branch": "trunk",
  "suite_id": "u-bh543",
  "suite_revision": "115701",
  "variant_label": "r1i1p1f2"
}
~~~

6. Begin the CDDS process:

  `source cdds_workflow_for_user.sh`

  Several directories will be created (their structure will be based on information in the json request file.) It is worth familiarizing yourself with the data structure and its relation to entries in the json request file.

  `cdds_data` will hold spaces for input and output data

  `ls $CDDS_DIR/cdds_data/CMIP6/AerChemMIP/UKESM1-0-LL/piClim-NTCF/r1i1p1f2/round-1-monthly`
  `input/	 output/`
  
  `cdds_proc` will contain various configuration files and logging output

  `ls $CDDS_DIR/cdds_proc/CMIP6/AerChemMIP/UKESM1-0-LL_piClim-NTCF_r1i1p1f2/round-1-monthly`
  `archive/  configure/  convert/	extract/  prepare/  qualitycheck/`
  
7. Tell CDDS where the input data resides by specifying its location (through soft links in this case) in the cdds_data directory. In our example, the raw data is in the aerchemmip group workspace

  `cd $CDDS_DIR/cdds_data/CMIP6/AerChemMIP/UKESM1-0-LL/piClim-NTCF/r1i1p1f2/round-1-monthly/input`
  `ln -s /gws/nopw/j04/aerchemmip_vol1/data/u-bh543_4archive u-bh543`
  
8. Enable the data conversion process - simply un-comment the final `cdds_convert` command in `cdds_workflow_for_user.sh`. A small amount of work will be repeated, but much of the structure already configured (in particular `cdds_data`) will persist. [ Note: this should be handled more elegantly through arguments to `cdds_workflow_for_user.sh` ]

  Several Rose suites will be created - monitor progress on `jasmin-cylc` with `cylc gscan`. Suite logging is in `cylc-run` as usual.

  Take a look in convert

  `ls convert`
  `log/  u-ak283_JSON/`

  `u-ak283-JSON` is the Rose suite that will run to perform the data conversions.

9. Converted data will be written to the output directory in cdds_data
~~~
  ls $CDDS_DIR/cdds_data/CMIP6/AerChemMIP/UKESM1-0-LL/piClim-NTCF/r1i1p1f2/round-1-monthly/output
  ap4/  ap4_concat/  ap4_mip_convert/  ap5/  ap5_concat/   ap5_mip_convert/
~~~

10. Consult the log files - cylc log files live under `/home/users/$USER/cylc-run/$SUITE_NAME` e.g. `/home/users/mrichardson001/cylc-run/cdds_UKESM1-0-LL_piClim-NOx_r1i1p1f2_ap4/log/job/18500101T0000Z/mip_convert_ap4_atmos-native/04/job.err` or `job.out` - it is important to note any possible cmor and/or mip_convert errors, and associated logs are written to the work directory e.g.
`/work/scratch/mrichardson001/cylc-run/cdds_UKESM1-0-LL_piClim-NOx_r1i1p1f2_ap5/work/18500101T0000Z/mip_convert_ap5_atmos-native/cmor.2019-12-10T1819Z.log.gz` - the actual log files are written in order of runs time and the `job.err` contains the pointer to the files in `/work`.

#### Variable Deactivation
If you need to deactivate variables you will have to run the deactivation between the Prepare and Configure steps. Deactivation can be done manually or via a [​script](#TODO) where you set your deactivation parameters, specifically the variables to be deactivated, or the file holding these variables and the message to be logged.

### 6. Quality Control

Login to one of the `jasmin-sci` machines. Change directory to `CDDS_DIR`.

Set up the CDDS environment (alternatively look at the last few lines of source `cdds_workflow_for_user.sh`):

`source /gws/smf/j04/cmip6_prep/cdds-env/setup_cdds_env.sh`

Set up the environment variables
~~~
REQUEST_JSON
USER_PROC=$CDDS_DIR/cdds_proc
USER_DATAROOT=$CDDS_DIR/cdds_data
~~~

Run the quality check utility:
~~~
qc_run_and_report $CDDS_DIR/$REQUEST_JSON -c $USER_PROC -t $USER_DATAROOT -p
~~~

Review the quality check output under `cdds_proc`
~~~
ls $CDDS_DIR/cdds_proc/CMIP6/FAFMIP/HadGEM3-GC31-LL_faf-heat_r1i1p1f1/round-1-monthly/qualitycheck
approved_variables_2019-10-08T113517.txt     log/     qc.db     report_2019-10-08T113517.json
~~~

### 7. Bookkeeping your runs
It is important to have a record of your run(s) both for debugging purposes and for knowing which runs have been done. For this purpose, please update the table here ​https://github.com/cedadev/jasmin-cdds/issues/31 and follow the instructions here ​https://github.com/cedadev/jasmin-cdds/tree/master/cdds_runs how to upload to gitHub the files that need to be logged and linked to the table. Contact V or Ag if any issues with github.

### 8. Move CMOR data to ESGF 

