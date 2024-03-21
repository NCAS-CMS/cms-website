---
layout: page-fullwidth
title: Ozone redistribution
teaser: Instructions for adding ozone redistribution to a GC3.1 suite
breadcrumb: true
---

## About ozone redistribution

The ozone redistribution (OR) scheme for GC3.1 is described here: https://doi.org/10.1029/2019MS001714

The code lives in the [moci repository](https://code.metoffice.gov.uk/trac/moci/wiki/OzoneRedistribution). 
It was ported to ARCHER2 by CMS, and works slightly differently than in the Met Office, 
due to the difference in infrastructure. 

## How it works in a suite

_This is just a technical outline of what the suite is doing. The science is descibed in the paper above._

The run must start from 1st January, and the cycle length can not be longer than 1 year. 

A new task `retrieve_ozone` runs before the UM, and checks the input data required for the OR code is available.  
It then sets up symlinks to the orography and ozone ancillary in a directory: `share/data/ozone_redistribution`.
It also sets up a symlink to the ozone file the model will use in: `share/data/etc/ozone`. 
For the first year of the run this is just the original ozone ancil. 

The UM uses an optional configuration (`app/um/opt/rose-app-ozone.conf`) which tells it to use the ozone file defined above. 
It also specifies some additonal STASH needed for the OR: 
```
(0, 253)  DENSITY*R*R AFTER TIMESTEP
(30, 453) Height at Tropopause Level
```
These are output as monthly means to a stream `po` with one file for the full year. 

At the end of the year, `postproc` converts these to pp format, and keeps two years worth of files on disk for processing. 

Then `retrieve_ozone` runs again. This time it adds in symlinks for the `po` file(s) in `share/data/ozone_redistribution`, 
and adds a symlink for the new ozone ancil file that the OR code will create (in `share/data/etc/ozone`). 

After this, the `redistribute_ozone` runs the actual OR code, which generates a new ozone ancillary file. 
The model runs the next year of the simulation using the updated file.

So the OR is not actually run until the end of the first year of the simulation, and then it just uses data from this first year. 
For subsequent years, it uses the previous two years worth of data. 
This is a bit different to the system at the Met Office, 
where data is extracted from MASS from a previous run 
so that the redistribution can be done before the start of the simulation.

## Adding ozone redistribution to a suite.

### 1. Upgrade postproc

Make sure postproc is using [version 2.4](unified-model/jdma.md#um-rose-suite-changes). 
If necessary set up [JASMIN transfer](unified_model/pptransfer/).
Test that postproc works correctly, then proceed to the next step.

### 2. Checkout the refrence suite.

The reference suite is `u-cr335`, which is an Eocene suite with the OR code working in it.
We will copy the new app files in from here.
```
rosie co u-cr335
```

### 3. Copy in the OR config files

Navigate to the suite you want to edit, and copy in the following files:
```
cd <your-suite>
cp -r ../u-cr335/app/redistribute_ozone ./app
cp -r ../u-cr335/app/retrieve_ozone ./app
cp ../u-cr335/app/install_ancil/opt/rose-app-ozone.conf ./app/install_ancil/opt
cp ../u-cr335/app/um/opt/rose-app-ozone.conf ./app/um/opt
cp ../u-cr335/bin/copy_ozone.sh ./bin
cp ../u-cr335/bin/python_env ./bin
cp -r ../u-cr335/meta/ozone ./meta
cp -r ../u-cr335/ozone-redistribution.rc .
cp -r ../u-cr335/site/archer2_ozone.rc ./site
cp -r ../u-cr335/site/archer2_python_env ./site
```

### 4. Make sure the OR configs are included

* Open `meta/rose-meta.conf` and add the following line to the top of the file:
```
import=meta/ozone
```

* In `rose-suite.conf` add the following lines to the top of the file:
```
[file:bin/redistribute_ozone.py]
source=fcm:ancil_contrib.xm_br/dev/simonwilson/r9929_ozone_pp_header/OzoneConc/bin/redistribute_ozone.py

[file:bin/redistribute_ozone.sh]
source=fcm:ancil_contrib.xm_br/dev/simonwilson/r9929_ozone_pp_header/OzoneConc/bin/redistribute_ozone.sh

[file:bin/retrieve_ozone_data.py]
source=fcm:moci.xm_tr/Utilities/ozone_redistribution/retrieve_ozone_data.py@postproc_2.4
```
* Then add the following lines to the list of variables:
```
OZONE_HOST='archer2'
OZONE_INITIAL='/work/n02/n02/ssteinig/ancils/PI/n96e/ozone/timeslice_1850/mmro3_monthly_CMIP6_1850_N96_edited-ancil_2anc'
OZONE_INPUT_SPLIT_ANCIL=false
!!OZONE_INPUT_SPLIT_NAME='/work/n02/n02/simon/canari/ozone/ancil/mmro3_monthly_CMIP6_\${THISYEAR}_N216_edited-ancil_2anc'
OZONE_PRIMARY_ARCHIVE='\${OZONE_STREAM_DIR}/\${OZONE_STREAM_PREFIX}'
OZONE_REDISTRIBUTE=true
OZONE_SECONDARY_ARCHIVE=''
OZONE_USE_UPDATED_ANCIL=false
```

* In `site/archer2.rc` add the following lines to the bottom of the file:
```
	{% include 'site/' + SITE + '_ozone.rc' %}
```

* In `suite.rc`, add the following line to the bottomr of the file, or above the [visualization] line if there is one:
```
	{% include 'ozone-redistribution.rc' %}
```

## Configuring the suite 

* Switch on 3D ozone. You will need a 3D ozone ancillary if you are not already using one in your suite.

* There is an "Ozone redistribution" section in the rose edit GUI, with some options. 
  Probably the only one you need to change is the "Initial ozone ancillary" which is the original 3D ozone file it's using.

* If you are changing the orography file, then you need to edit `site/archer2_ozone.rc`
  and change `UM_MODEL_ANCILS_LINK` - this is the top-level directory for the ancils.

* Check the paths to the orography

* Check the output streams

* Make sure the run starts from 1 Jan of the year, and the cycle length is less than a year.

The OR scheme is quite complicated, and your suite may require some additional changes to get it working properly. 
Contact the helpdesk if you require advise. 

## Checking the output

Follow the technical description above (link) and check that the correct links are being set up at each stage. When you think that you have the scheme working, take a look the output dump from a cycle when OR is active to ensure that the correct ozone ancil is being read in by the model. 
The ozone at heights ~10000 should look like whats below. 
There should be some horizontal banding added in by the OR; 
if there's no banding, then something's gone wrong somewhere. 

<add image>
