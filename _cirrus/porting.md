---
layout: page-fullwidth
title: Porting
subheadline: Porting a UM Suite to Cirus
permalink: '/cirrus/porting/'
breadcrumb: true
---

Unfortunately as UM suites can be configured in many ways and there's no "standard" UM suite setup it is difficult to provide a comprehensive set of porting instructions.  We provide a ["quick start"]({{'/cirrus/porting/quick-stat/' | relative_url }}) guide which should be appropriate for most UM13.x versions and then further detailed guidance covering changes to the suite site `*.rc`/`*.cylc` files for the move to Cirrus.

* [General Guidance]({{'/cirrus/porting/general-info/' | relative_url }})
* [Quick Start Instructions]({{'/cirrus/porting/quick-start/' | relative_url }})
* [Detailed information on how to change a site/archer2.rc file to site/cirrus.rc]({{ '/cirrus/porting/detailed/' | relative_url }})
* [Post Processing and Data Transfer to JASMIN]({{ '/cirrus/porting/postproc-pptransfer' | relative_url }})

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

## General Guidance

### Setting up connection to PUMA2

It is no longer possible to use a passphraseless key to connect from Cirrus login nodes to PUMA2.  The recommended method to login to PUMA2 is by using port-forwarding;  this is setup is also required in order to use the Cylc 8 web UI. Please see [Connection to PUMA2 via Cirrus](https://cms-helpdesk.ncas.ac.uk/t/connecting-to-puma2-via-cirrus/2232) on the CMS Helpdesk. Please do not use ssh-agent forwarding as this can cause problem with Cylc. 

### Setting up environment on Cirrus

Make sure you have the following line in your `~/.bash_profile` on Cirrus:

```
# Setup environment for running the UM under Rose
. /work/y07/shared/umshared/bin/rose-um-env-puma2
```

### Efficient use of Cirrus Compute Nodes





