---
layout: page-fullwidth
title: Ozone redistribution
teaser: Instructions for adding ozone redistribution to a GC3.1 suite
permalink: '/unified-model/ozone-redistribution/'
breadcrumb: true
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

## Overview

The ozone redistribution (OR) scheme for GC3.1 (CMIP6) is described in a paper by [Hardiman, 2019](https://doi.org/10.1029/2019MS001714). 
The Met Office also have [documentation](https://code.metoffice.gov.uk/trac/moci/wiki/OzoneRedistribution) for a how the OR works in a suite. 

These instructions are for adding OR to a GC3.1 suite on Archer2. If you have a GC5 suite, it may have OR already included but changes will be required to run on Archer2. Alternatively you may find it easier to use one of the refernce suites as a starting point. 

See the reference suites for working examples: 

| Config | Suite |
| :----- | :---- |
| GC3.1  | [u-as037/ozone_redistribution](https://code.metoffice.gov.uk/trac/roses-u/browser/a/s/0/3/7/ozone_redistribution) | 
| GC5    | [u-da412/archer2_ozone](https://code.metoffice.gov.uk/trac/roses-u/browser/d/a/4/1/2/archer2_ozone) | 

## Ozone redistribution in a suite 

See also this [description of the ozone redistribution scheme](https://code.metoffice.gov.uk/trac/moci/wiki/OzoneRedistribution)

The OR requires several new tasks to be added to the suite, and changes made to some exisitng tasks. The diagram below shows the graph of a suite which includes OR.

![Graph of suite with ozone redistribution]({{site.urlimg}}ozone_graph.png)

* `coupled`: As the model runs, data required for the OR is written to a monthly `p4` file: 
```
(0, 253)  DENSITY*R*R AFTER TIMESTEP
(30, 453) Height at Tropopause Level
```

* `postproc`: The monthly `p4` files are then gathered into an annual `po` file for use by the OR code. 
 
* `retrieve_ozone`: This runs at the start of the year before the model and checks that input data required for the OR code are available. The scheme requires data from the previous 1 or 2 years of the simulation. This may be from this run or archived data. Source data is symlinked into a directory: `share/data/ozone_redistribution`. If no archived data is available the OR scheme will not be run for the first year. 

* `redistribute_ozone`: Runs the actual redistribution code, creating a new ozone ancillary file for use in the next year of the simulation in: `share/data/etc/ozone`

* `rose_arch_zone`: Archives the newly created ancillary file and clears out the `share/data/ozone_redistribution` directory. 

* `coupled`: When the subsequent model task runs it will use the updated ozone ancillary file. 

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

## Adding ozone redistribution to a suite.

### 1. Upgrade postproc

Make sure postproc is using version 2.4, and if necessary set up JASMIN transfer.
Test that this works correctly before proceeding to the next step.

### 2. Checkout the reference suite.

For GC3.1 the reference suite is `u-as037/ozone_redistribution`. Note that `u-as037` is based on Met Office suite-id u-ar766, the CMIP6 pre-industrial control config at N96-ORCA1 - see [CMIP6 standard jobs](https://code.metoffice.gov.uk/trac/ukcmip6/wiki/StandardJobs). 
```
rosie co u-as037/ozone_redistribution
```

### 3. Copy in the OR configuration files

Copy these apps from the reference suite into the corresponding location in your suite:
```
app/ants_package_build/*
app/contrib_package_build/*
app/redistribute_ozone/*
app/retrieve_ozone/*
app/redistribute_ozone/*
app/retrieve_ozone/*
app/rose_arch_ozone/*
```

Copy in these files: 
```
app/postproc/opt/rose-app-ozone.conf
app/um/opt/rose-app-ozone.conf
meta/ozone/rose-meta.conf
ozone_redistribution.rc
site/archer2_ozone.rc
site/archer2_python_env
```

### 4. Add in the include files and suite variables. 

* Open `meta/rose-meta.conf` and add the following line to the top of the file:
```
import=meta/ozone
```

* In `rose-suite.conf` add the following lines to the top of the file:
{% raw %}
~~~
[file:bin/retrieve_files.sh]
source=fcm:moci.xm_br/dev/annetteosprey/postproc_2.4_archer2_ozone/Utilities/ozone_redistribution/retrieve_files.sh

[file:bin/retrieve_ozone_data.py]
source=fcm:moci.xm_br/dev/annetteosprey/postproc_2.4_archer2_ozone/Utilities/ozone_redistribution/retrieve_ozone_data.py
~~~
{% endraw %}

* Then add the following lines to the list of variables (we will configure these settings in the next step):

```
OROG_ANCIL='\${UMDIR}/ancil/atmos/n96e/orca1/orography/globe30/v6/qrparm.orog'
OZONE_ANCIL_INITIAL='\${CMIP6_ANCILS}/n96e/timeslice_1850/OzoneConc/v1/mmro3_monthly_CMIP6_1850_N96_edited-ancil_2anc'
OZONE_HOST='archer2'
OZONE_PRIMARY_ARCHIVE=''
OZONE_REDISTRIBUTE=true
OZONE_SECONDARY_ARCHIVE=''
OZONE_SKIP_FIRST_YEAR=true
OZONE_USE_UPDATED_ANCIL=false
```

* In `site/archer2.rc` add the following lines to the bottom of the file:
```{% raw %}
	{% include 'site/' + SITE + '_ozone.rc' %}
{% endraw %}```

* In `suite.rc`, add the following line to the bottom of the file, or above the [visualization] line if there is one:
```{% raw %}
	{% include 'ozone-redistribution.rc' %}
{% endraw %}```

### 5. Configure the suite

In the rose edit GUI, under "suite conf -> Ozone redistribution", you will find options for the OR scheme.

* "Host machine for ozone redistribution" should be set to "archer2". 

* Set "Initial ozone ancillary" to be your ozone ancillary file. If the file is very large and takes a long time to load in iris, ou can split it into individual years (contact the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk) for advice on this).

* Set "Orography ancillary" to be the full path and filename for the orography ancillary file used in the suite. To work out what this is, check the `install_ancil` app and potentially the optional configs. 

* Leave "Skip ozone redistribution in first year" as "false", unless you ozone files from a previous run.

* If you do have archived files, specify the path to the files in "Primary archive source", e.g.:
{{{
OZONE_PRIMARY_ARCHIVE='/work/n02/n02/annette/archive/u-as037-ozone/18520101T0000Z/as037a.po'
}}}

Additionally you may need to check the following options: 

* The standard code requires you to use a 3D ozone ancillary file. If this is not already set up, then set the following variables in `app/um/rose-app.conf` or in the um section of the `rose edit` GUI:
```
  zon_av_ozone=.false.
  i_ozone_int=1
```
  You will also need to make sure and specify a 3D ozone ancil in the "Initial ozone ancillary" option above. 

* Check the UM output streams. By default the new `p4` stream goes to a file id `pp104` and usage profile `UP4`. In `u-as037` this stream already exists, so the optional config increses the number of reserved headers in  `app/um/opt/rose-app-ozone.conf`. If this stream does not exist you should set `reserved_headers=0`.

* Check that the base of the archiving path in `rose_arch_ozone/opt/rose-app-archer2.conf` matches the location in postproc `archive_root_path`, e.g:
{{{

}}}

The OR scheme is quite complicated, and your suite may require some additional changes to get it working properly. 
Contact the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk) if you need advice.

## Checking the output

Follow the technical description above (link) and check that the correct links are being set up at each stage. 

When you think that you have the scheme working, take a look the output dump from a cycle when OR is active to ensure that the correct ozone ancil is being read in by the model. The ozone at heights ~10000 should look like the image below. (For PI runs it may be around height ~9000.)
There should be some horizontal banding added in by the OR; if there's no banding, then something's gone wrong somewhere.

![Ozone at ~ 10,000 after redistribution]({{site.urlimg}}ozone_redist.png)
