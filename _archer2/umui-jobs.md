---
layout: page-fullwidth
title: Running UMUI Jobs on ARCHER2
subheadline: ARCHER2
permalink: '/archer2/umui/'
breadcrumb: true
---
Only UMUI versions 7.3 & 8.4 are supported on ARCHER2.

{% include alert note='Note: Post Processing has not been tested.' %}

### Initial setup

1. Add the following snippet to your ARCHER2 `~/.bash_profile`:
```
   # Setup UM Variables
   VN=7.3 ## or 8.4 as appropriate
   if test -f $HOME/.umsetvars_$VN; then
     . $HOME/.umsetvars_$VN
   else
     . /work/y07/shared/umshared/vn$VN/cce/scripts/.umsetvars_$VN
   fi
```

2. Setup `umui_runs` directory:
```
   archer2$ mkdir /work/n02/n02/<archer2_username>/umui_runs
   archer2$ ln -s /work/n02/n02/<archer2_username>/umui_runs ~/umui_runs
```

Very few changes are required in order to run these jobs:

### UM 8.4

* In *Model Selection → User Information and Submit method → Job submission method*
    * Select submission method: **SLURM Cray EX (ARCHER2)**
    * Set **Host name** to `login.archer2.ac.uk`
    * Set the number of processors to be a multiple of 128
    * Click the **Slurm** button to specify the Job time limit <br>
    <br>

* In *Model Selection → FCM Configuration → FCM Extract directories and Output levels*
    * Set **Target machine root directory (UM_ROUTDIR)** to a location on `/work` (e.g. `/work/n02/n02/$USERID/um`) <br>
    <br>

* In *Model Selection → Input/Output Control and Resources → Time Convention and SCRIPT Environment Variables*
    * Set `DATADIR` in the **Defined Environment Variables** table. This must be on `/work` (e.g. `/work/n02/n02/<username>`)
    * Ensure **DATAM** and **DATAW** are set to a location on `/work`. E.g `$DATADIR/um/$RUNID` 

### UM 7.3

* In *Model Selection → User Information and Target Machine → Target Machine*
    * Set **Machine name** to `login.archer2.ac.uk`
    * Set the number of processors to be a multiple of 128 
    <br><br>
* In *Model Selection → Input/Output Control and Resources → Time Convention and SCRIPT Environment Variables*
    * Set `DATADIR` in the **Defined Environment Variables** table. This must be on `/work` (e.g. `/work/n02/n02/<username>`)
    * Ensure **DATAM** and **DATAW** are set to a location on `/work`. E.g `$DATADIR/um/$RUNID` 
    <br><br>
* In *Model Selection → Input/Output Control and Resources → Job submission, resources and re-submission pattern*
    * Select submission method: **SLURM Cray EX (ARCHER2)**
    * Note - the model will not recognize a change to the default number of cores/node 
    <br><br>
* In *Model Selection → FCM Extract and Build directories and Output levels*
    * Set **Target machine root directory (UM_ROUTDIR)** to a location on `/work` (e.g. `/work/n02/n02/ros/um`) 
    <br><br>
* In *Model Selection → Compilation and Modifications → UM User Override Files*
    * The **User machine overrides** must use `~umui/overrides/archer2_cce_7.3_machine`
    * The **User file overrides** must use `~umui/overrides/archer2_cce_7.3_file`


