---
layout: page-fullwidth
title: Quick Start
subheadline: Porting a UM suite to ARCHER2
permalink: '/archer2/porting/quick-start/'
breadcrumb: true
---
The following should be appropriate for most UM vn11.x versions. Unfortunately as UM suites can be configured in multiple ways and there's no "standard" UM job configurations it cannot be guaranteed to work. If there are still issues, please reference the more [detailed instructions]({{ '/archer2/porting/detailed' | relative_url }}).

There are 4 stages in converting an ARCHER suite into an ARCHER2 suite:

* Copy a standard `archer2.rc` site file.
* Edit the `suite.rc` to use this file.
* Edit the metadata file to add ARCHER2 options.
* Update the suite to use ARCHER2 and change the processor decomposition. 

First, copy the suite you wish to run on ARCHER2, check it out and `cd` into its rose directory. Then, taking each of the above in turn:

### archer2.rc

#### Atmosphere only suites

Firstly look at your `suite.rc` file.

If it has lines of the form `UM_ATM_NPROCX = {% raw %}{{MAIN_ATM_PROCX}}{% endraw %}` with a `MAIN_` pre-pending the variable then copy `/home/simon/archer2/archer2.rc_main` to `site/archer2.rc`.

If it has lines of the form `UM_ATM_NPROCX = {% raw %}{{ATM_PROCX}}{% endraw %}` then copy `/home/simon/archer2/archer2.rc` to `site/archer2.rc`.

If the `UM_ATM_NPROCX =` type lines use some other format, copy `/home/simon/archer2/archer2.rc` as a base and then edit it to change each line in:
```{% raw %}
{% set APPN = ATM_PPN if ATM_PPN is defined else PPN %}
{% set TASKS_RCF = RCF_PROCX * RCF_PROCY %}
{% set TASKS_ATM = ATM_PROCX * ATM_PROCY + IOS_NPROC %}
{% set NODE_RCF = node(TASKS_RCF, OMPTHR_RCF, HYPTHR_RCF, APPN) %}
{% set NODE_ATM = node(TASKS_ATM, OMPTHR_ATM, HYPTHR_ATM, APPN) %}
{% set TPNUMA_RCF = tpnuma(OMPTHR_RCF, HYPTHR_RCF, APPN, NUMA) %}
{% set TPNUMA_ATM = tpnuma(OMPTHR_ATM, HYPTHR_ATM, APPN, NUMA) %}
{% endraw %}```
so that the variables match the equivalents in the `suite.rc` file.

Edit the line

 `--chdir=/work/n02/n02/<username>`

to use your ARCHER2 username in the copied `archer2.rc`.

Users of vn11.7 may have to change `EXPT_HORIZ` to `EXPT_HORIZ_ATM` in `archer2.rc`

#### Coupled and UKESM jobs

Copy `/home/simon/archer2/archer2.rc_ukesm` to `site/archer2.rc`.

Edit the line

 `--chdir=/work/n02/n02/<username>`

to use your archer username in the copied `archer2.rc`.

Note as the Coupled configuration is more complicated than the atmosphere only configuration, there's a greater possibility that the `archer2.rc` file will need further modifications. Please see the more [detailed documentation]({{ '/archer2/porting/detailed' | relative_url}}).

### suite.rc

Search the `suite.rc` for any reference to **archer**. If there are none, go onto the next step. Otherwise, change each instance of a reference to `archer` with `archer2`.

For example change

`{% raw%}{% set KNOWN_SITE_CFGS = ['archer', 'meto_cray', 'monsoon', 'nci_raijin', 'niwa_cray'] %}{% endraw %}`

to

`{% raw%}{% set KNOWN_SITE_CFGS = ['archer2', 'meto_cray', 'monsoon', 'nci_raijin', 'niwa_cray'] %}{% endraw %}`

Note: If the line

`{% raw%}{% include site/archer-tests.rc %}{% endraw %}`

is present, do not change it.

### Metadata

In `meta/rose-meta.conf`, locate and change all instances of `archer` to `archer2`, `ARCHER` to `ARCHER2`, `Archer` to `Archer2`, etc.

For example:
~~~
[jinja2:suite.rc=ARCHER_GROUP]
compulsory=true
description=
help=Account code under which to run HPC tasks (e.g. n02-ncas)
ns=host
sort-key=archer_2
title=Account group for HPC tasks
~~~
should be updated to
~~~
[jinja2:suite.rc=ARCHER2_GROUP]
compulsory=true
description=
help=Account code under which to run HPC tasks (e.g. n02-ncas)
ns=host
sort-key=archer2_2
title=Account group for HPC tasks
~~~
Also, in `[jinja2:suite.rc=MAIN_ATM_PPN]` or `[jinja2:suite.rc=ATM_PPN]` change `range=1:36` to `range=1:128`

### GUI

Now start up the `rose edit` GUI. There will be a warning triangle next to the **suite conf** section. We need to fix the errors to get rid off the warning triangles.
 * In *suite conf→Host Machine*:
   * Set **Site** to be **Archer2**
   * Set the **Queue** to **Standard**
   * Set **Account group** by clicking on the plus sign to add it to the configuration, and then set to the required value. \\
   Note: This may be contained in a separate *Project Accounting* panel. Remember to put the account group in single quotes. 

 * In *suite conf→Domain Decomposition*:
   * Set the **Max number of processors/node** to be **128**. If you plan to depopulate the node, set this to some multiple of 16. \\
If not using IO servers, it is also a good idea to change the **Atmosphere decomposition** so that the NSxEWx(OpenMP threads) is some multiple of 128 for most efficient running. Keep the total number of cores roughly the same as for ARCHER.

 * In *fcm_um_make→env→Configuration file*:
   * Set **config_root_path** to `fcm:um.xm_br/dev/simonwilson/vn11.x_archer2_compile` \\
     where **x** is the UM version of the suite.
   * Remove the revision number from **config_revision** so that the field is blank.

 * For vn11.1 and vn11.2 jobs in *fcm_um_make→env*:
   * In **Sources** add the branch `fcm:um.x_br/dev/jeffcole/vn11.x_archer2_fixes` \\
   where x is the UM version of the suite.

 
 * In *suite conf→Tasks*:
   * Ensure that **Run Development Tests** is set to false as these don't currently work on ARCHER2.

**Save** the changes.

Note: If you have any bespoke ARCHER app conf files (possibly set in Model Configuration), these may have to be renamed and updated for ARCHER2

You should now able to submit the suite to ARCHER2.

