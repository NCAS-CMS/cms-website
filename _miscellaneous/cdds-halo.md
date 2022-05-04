---
layout: page-fullwidth
title: CDDS Halo
teaser: Documentation on how to remove halos from datasets before converting data using CDDS.
---
Suite `u-bo201` is built to remove halos from datasets.  The following steps are necessary prior to converting data using CDDS.  This suite can be found in the MOSRS repository using `rosie go`.

### Step 1:

Log into JASMIN cylc server (`cylc.jasmin.ac.uk`)

### Step 2:

Copy suite `u-bo201` and change two variables within the `rose-suite.conf` file; `HALO_START_DIR` and `root-dir{work}`:

 1) **HALO_START_DIR**
  
This is where your data sits prior to being put through the de-halo process. The path expects a suite directory which itself contains directories with data files.

The following example shows how to specify your HALO_START_DIR path:

`HALO_START_DIR = /gws/nopw/j04/rdf_migrate_vol2/my_username/u-aa123`

![Suite Structure](/images/cdds-halo-suite-structure.png)

 2) **root-dir{work}**
 
This is the location where the cylc-run/work directory will be created during the run. The cylc-run/work directory is used as an intermediate space to store data files while they are being de-haloed. This must be set to a location on the same group workspace as HALO_START_DIR i.e.

`root-dir{work}=*=/path/to/gws/my_username`

### Step 3:

Run the suite.

The suite will start one cycle run per directory being put through the de-halo process. A cycle will fail during ‘file_check’ if it cannot find a corresponding directory.

As part of suite workflow, a `cdds-holding` directory will be generated which temporarily holds files. NEVER delete anything from the `cdds-holding` direcory - contact CMS is you suspect a problem.

What you end up with:

1) Your `HALO_START_DIR` still contains all of your original directories, but these directories now only contain the original versions of `.nc` files which needed de-haloing.

2) A new directory with the same name as the start directory, but which ends in `-cdds` (i.e. `u-aa123-cdds`) . This directory gets created at the start of the suite run at the same path location as the `HALO_START_DIR`. This will contain all of your data with the new `.nc` files which have been de-haloed.



