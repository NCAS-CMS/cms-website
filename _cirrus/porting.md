---
layout: page-fullwidth
title: Porting
subheadline: Porting a UM Suite to Cirus
permalink: '/cirrus/porting/'
breadcrumb: true
---

Unfortunately as UM suites can be configured in many ways and there's no "standard" UM suite setup it is difficult to provide a comprehensive set of porting instructions.  We provide a ["quick start"]({{'/cirrus/porting/quick-stat/' | relative_url }}) guide which should be appropriate for most UM13.x versions and then further detailed guidance covering changes to the suite site `*.rc`/`*.cylc` files for the move to Cirrus.

* [General Guidance]({{'/cirrus/porting/general-guidance/' | relative_url }})
* [Quick Start Instructions]({{'/cirrus/porting/quick-start/' | relative_url }})
* [Detailed information on how to change a site/archer2.rc file to site/cirrus.rc]({{ '/cirrus/porting/detailed/' | relative_url }})


## Ported UM Workflows

The following workflows have been updated for Cirrus.

| UM version | Suite id | Description | Branches + Notes |
| ---------- | -------- | ----------- | ---------------- |
| 13.8 | u-do527/cirrus | GAL9 |  |
| 13.8 | u-dx690/cirrus | UKCM2 (GC5) | |
| 13.9 |  | UKESM1.1 AMIP | |
| 13.9 | u-dr681/cirrus | UKESM1.1 PI Control | In `app/fcm_make_ocean/file/fcm-make.cfg` add <br> <br> `build-ocean.prop{fc.flags}[nemo/NEMOGCM/NEMO/OPA_SRC/IOM/iom_nf90.F90] = $fcflags_nemo_common -O0 -Ovector1 -hfp0 -hflex_mp=strict -hipa0 -G1 $fcflags_omp $fcflags_coupling`  |
| 13.9 | u-dr682/cirrus | UKESM1.1 Historical | In `app/fcm_make_ocean/file/fcm-make.cfg` add <br> <br> `build-ocean.prop{fc.flags}[nemo/NEMOGCM/NEMO/OPA_SRC/IOM/iom_nf90.F90] = $fcflags_nemo_common -O0 -Ovector1 -hfp0 -hflex_mp=strict -hipa0 -G1 $fcflags_omp $fcflags_coupling` |

* Note, for example, u-do527/cirrus indicates the cirrus branch of u-do527.*






