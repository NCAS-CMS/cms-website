---
layout: page-fullwidth
title: Ozone redistribution
teaser: Instructions for adding ozone redistribution to a GC3.1 suite
permalink: '/unified-model/ozone-redistribution/'
breadcrumb: true
---

## About ozone redistribution

The ozone redistribution (OR) scheme for GC3.1 used in CMIP6 is described here: https://doi.org/10.1029/2019MS001714

The code lives in the [moci repository](https://code.metoffice.gov.uk/trac/moci/wiki/OzoneRedistribution). 
It was ported to ARCHER2 by CMS, and works slightly differently than in the Met Office, 
due to the difference in infrastructure. 

## How it works in a suite

_This is just a technical outline of what the suite is doing. The science is descibed in the paper above._

The run must start from 1st January, and the cycle length can not be longer than 1 year. 

A new task `retrieve_ozone` runs before the UM, and checks the input data required for the OR code is available.  
It then sets up symlinks to the orography and ozone ancillary in a directory: `share/data/ozone_redistribution`.
It also sets up a symlink to the ozone file the model will use for the first year of the simulation in `share/data/etc/ozone`. 
This just points to the original ozone ancil. 

The UM uses an optional configuration (`app/um/opt/rose-app-ozone.conf`) which tells it to use the ozone file defined above. 
It also specifies some additonal STASH needed for the OR: 
```
(0, 253)  DENSITY*R*R AFTER TIMESTEP
(30, 453) Height at Tropopause Level
```
These are output as monthly means to a stream `po` with one file for the full year. 

At the end of the year, `postproc` converts these to pp format, and keeps two years worth of files on disk for processing. 

Then `retrieve_ozone` runs again. This time it adds in symlinks for the `po` file(s) in `share/data/ozone_redistribution`. 
and adds a symlink for the new ozone ancil file that the OR code will create (in `share/data/etc/ozone`). 

After this, the `redistribute_ozone` runs the actual OR code, which generates a new ozone ancillary file for the next model year in `share/data/etc/ozone`. 

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

### 3. Copy in the OR configuration files

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

### 4. Add in the include files and suite variables. 

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

* Then add the following lines to the list of variables (we will configure these settings in the next step):
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
```{% raw %}
	{% include 'site/' + SITE + '_ozone.rc' %}
{% endraw %}```

* In `suite.rc`, add the following line to the bottomr of the file, or above the [visualization] line if there is one:
```{% raw %}
	{% include 'ozone-redistribution.rc' %}
{% endraw %}```

### 5. Configure the suite 

* Make sure the run starts from 1 Jan of the year, and the cycle length is a year or less.

* The standard code requires you to use a 3D ozone ancillary file. If this is not already set up, then set the following variables in `app/um/rose-app.conf` or in the um section of the `rose edit` GUI:
```
  zon_av_ozone=.false.
  i_ozone_int=1
```

* In the rose edit GUI, under "suite conf -> Ozone redistribution", set "Initial ozone ancillary" to be your 3D ozone ancillary file. If the file is large because it contains a long time-series this can slow down the code so we recommend you can split it into individual years (contact the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk) for advice on this). In this case you should select "Use split input ozone ancillaries", then edit "Name of split input ancillaries" as in the example below: 
```
/work/n02/n02/simon/canari/ozone/ancil/mmro3_monthly_CMIP6_\${THISYEAR}_N216_edited-ancil_2anc
```

* Check the name and location of the orography file used in the suite. If the top-level location is anything other than `$UMDIR/ancil`, then edit the variable `UM_MODEL_ANCILS_LINK` in `site/archer2_ozone.rc`. Next check the path set in `app/retrieve_ozone/rose-app.conf` as below. (Note that this may also be specified using an optional configuration.)
```
[file:$OZONE_SHARE/qrparm.orog]
mode=symlink+
source=${UM_MODEL_ANCILS_LINK}/orography/globe30/qrparm.orog
```

* Check the UM output streams. By default the new `po` stream goes to a file id `pp145` and usage profile `UPO`. If these clash with existing settings in your suite, you will need to rename them in `app/um/opt/rose-app-ozone.conf`. 

* Set up postproc to convert the `po` stream to pp, and make sure it is saved on disk for the OR. In "postproc -> Atmosphere", either set `process_all_stream=true`, or make sure `po` is in the list under `process_streams`. Under "Atmosphere -> File transformation" make sure the `po` stream is being converted to pp, usually with `convert_pp=true` and `convpp_all_streams=true`. Next set `preserve_ozone=true` and `ozone_source_stream=po`. 

The OR scheme is quite complicated, and your suite may require some additional changes to get it working properly. 
Contact the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk) if you need advice. 

## Checking the output

Follow the technical description above (link) and check that the correct links are being set up at each stage. 

When you think that you have the scheme working, take a look the output dump from a cycle when OR is active to ensure that the correct ozone ancil is being read in by the model. 
The ozone at heights ~10000 should look like whats below. 
There should be some horizontal banding added in by the OR; 
if there's no banding, then something's gone wrong somewhere. 
