---
layout: page-fullwidth
title: Quick Start
subheadline: Porting a UM suite to Cirrus
permalink: '/cirrus/porting/quick-start/'
breadcrumb: true
---
The following should be appropriate for most UM vn13.x versions. Unfortunately as UM suites can be configured in multiple ways and there's no "standard" UM job configurations it cannot be guaranteed to work. If you have any problems please contact the CMS Helpdesk. 

There are 4 stages in converting an ARCHER suite into a Cirrus suite:

 * Edit the `flow.cylc` file to add Cirrus.
 * Copy the `archer2.rc` or `archer2.cylc` site file to `cirrus.rc` or `cirrus.cylc` and update for Cirrus.
 * Edit the metadata file to add Cirrus options.
 * Update the suite to use Cirrus and change the processor decomposition.

First, copy the suite you wish to run on ARCHER2, check it out and `cd` into its rose directory. Then, taking each of the above in turn:

### flow.cylc

Search the `flow.cylc` for any reference to **archer2**. If there are none, go onto the next step. Otherwise, change each instance of a reference to `archer2` with `cirrus`.

For example change

`{% raw%}{% set L_REMOTE_SETUP = true if SITE == 'archer2' else false %}{% endraw %}`

to

`{% raw%}{% set L_REMOTE_SETUP = true if SITE == 'cirrus' else false %}{% endraw %}`

### Cirrus Site File

Your suite will either have a site/archer2.rc or site/archer2.cylc file.

Copy this to either `site/cirrus.rc` or `site/cirrus.cylc` and edit as follows:

* Change the line `{% set PPN = 128 %}` to `{% set PPN = 288 %}`
* Change all occurrences of `/work/y07/` to `/epccfs/y07/` and `/work/n02` to `/epccfs/n02`
* If present change `module load cce/15.0.0` to `module load um`
* Replace all occurrences of `archer2` with `cirrus` \\
  For example change: \\
  `platform = archer2` to `platform = cirrus` and `platform = archer2-bg` to `platform = cirrus-bg`
* Replace all occurrences of `ARCHER2` with `CIRRUS`
  For example change: \\
  `--qos={{ARCHER2_QUEUE}}` to `--qos={{CIRRUS_QUEUE}}`
* Change `ncas-ex-cce` to `ncas-cirrus-cce`
* In section `[[HPC_SERIAL]] ` remove the lines containing `--partition=serial` and `--qos=serial`
* In section `[[RCF_RESOURCE]]` remove the lines `--tasks-per-node={{APPN}}` and `--cpus-per-task=1`
* Remove any occurrence of `--mem =`  For example in the section `[[UMBUILD_RESOURCE]]`

**Atmosphere only suites**

* In section `[[ATMOS_RESOURCE]][directives]` add the line `--exclusive=""`

**Coupled suites**

* In section `[[COUPLED_RESOURCE]][directives]` add the line `--exclusive=""` 
   
### Metadata

In `meta/rose-meta.conf`, locate and change all instances of `archer2` to `cirrus`, `ARCHER2` to `CIRRUS`, `Archer2` to `Cirrus`, etc.

For example:
~~~
[template variables=ARCHER2_GROUP]
compulsory=true
description=
help=Account code under which to run HPC tasks (e.g. n02-ncas)
ns=host
sort-key=archer2_2
title=Account group for HPC tasks
~~~
should be updated to
~~~
[template variables=CIRRUS_GROUP]
compulsory=true
description=
help=Account code under which to run HPC tasks (e.g. n02-ncas)
ns=host
sort-key=cirrus_2
title=Account group for HPC tasks
~~~

### GUI

Now start up the `rose edit` GUI. There will be a warning triangle next to the **suite conf** section. We need to fix the errors to get rid of the warning triangles.  You will likely need to click on the plus sign next to each of the settings below to add it to the configuration.
 * In *suite conf→Host Machine*:
   * Set **Site** to be **Cirrus**
   * Set the **Queue** to **Standard**
 * In *suite conf->Host Machine*:
   * Set **Account group**  to the required value.
   * Set **User account** to be your Cirrus username
Note: *Account group* and *user account* may be contained in the *Host Machine* panel. 

 * In *suite conf -> Domain Decomposition*:
   * Set the **Max number of processors/node** to be **288**.
   * Change the **Atmosphere decomposition** so that the NSxEWx(OpenMP threads) is some multiple of 288 for most efficient running. Keep the total number of cores roughly the same as for ARCHER2.

**IMPORTANT**: Please read the [guidance] on node usage for Cirrus. As Cirrus nodes are large it is very important to configure jobs correctly to not waste resources, not doing this could be costly to your project. 
  
 * In *fcm_make_um -> Configuration file*:
   * Set **config_root_path** to `fcm:um.xm_br/dev/jonnyhtwilliams/vn1X.Y_cirrus_compile` \\
     where **X.Y** is the UM version of the suite. 
   * Remove the revision number from **config_revision** os that the field is blank.
Note: If your suite uses optional configurations you may need to change this in the `app/fcm_make_um/rose-app-cirrus.conf` file.

**Save** the changes.

### General Suite changes

 * Update any input file paths as appropriate E.g. Change `/work` to `/epccfs`
 * If your suite contains optional configuration override files for ARCHER2 (named `rose-app-archer2.conf`) you will need to copy these to `rose-app-cirrus.conf` and update as appropriate.  To find all `rose-app-archer2.conf` files in your suite run:
   * `cd ~/roses/<suite-id>
   * ` find . -name rose-app-archer2.conf -print`

You should now be able to submit the workflow to Cirrus.

