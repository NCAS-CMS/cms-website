---
layout: page-fullwidth
title: Porting
subheadline: Porting a UM Suite to ARCHER2
permalink: '/archer2/porting/'
breadcrumb: true
---

### Rose/Cylc Suites

Unfortunately as UM suites can be configured in many ways and there's no "standard" UM suite configurations it is difficult to provide a comprehensive set of porting instructions.  We provide a ["quick start"]({{ '/archer2/porting/quick-start/' | relative_url }}) guide which should be appropriate to most UM11.x versions and then further detailed guidance covering changes to the suite `*.rc` for the move to the SLURM Scheduler.

* [Quick Start Instructions]({{ '/archer2/porting/quick-start/' | relative_url }})
* [Detailed information on changes to *.rc files]({{ '/archer2/porting/detailed' | relative_url }})
* [Post Processing]({{ '/archer2/porting/postproc-pptransfer' | relative_url }})
* [Data Transfer to JASMIN]({{'/unified-model/pptransfer' | relative_url }})

**Ported UM Suites**

| UM version | Suite id | Description | Branches + Notes |
| ---------- | ------------ | ----------- | ----- |
| 10.7 | u-as037 | HadGEM3-GC3.1 N96ORCA1 PI Control for CMIP6 | Replace the nemo_sources branch `dev_r5518_GO6_package` with working copy `/home/ros/nemo/branches/dev_r5518_GO6_package` to fix nemo_alloc problem <br> <br>Set ocean `ldflags_overrides_suffix` to `-lstdc++` |
| 11.1 | u-be303/archer2 | UKESM AMIP  | fcm:um.x_br/dev/jeffcole/vn11.1_archer2_fixes |
| 11.1 | u-ca103 | Nesting suite | fcm:um.x_br/dev/jeffcole/vn11.1_archer2_fixes |
| 11.1 | u-bu108 | KPP coupled India domain | fcm:um.x_br/dev/jeffcole/vn11.1_archer2_fixes <br> fcm:kpp_br/dev/annette/r194_r183_couple_flags_OMP_archer2  |
| 11.2 | u-be463/archer2 | GA7.0 N96 UM11.2 AMIP Climate Development (1988 - 2008) |fcm:um.x_br/dev/jeffcole/vn11.2_archer2_fixes |
| 11.2 | u-bc964/archer2 | UKESM coupled PI control | fcm:um.x_br/dev/jeffcole/vn11.2_archer2_fixes <br><br> cpmip analysis not currently working <br><br> set ocean `ldflags_overrides_suffix` to `-lstdc++` |
| 11.2 | will be u-bc613/archer2 | UKESM coupled Historical | fcm:um.x_br/dev/jeffcole/vn11.2_archer2_fixes <br><br> cpmip analysis not currently working <br><br> set ocean `ldflags_overrides_suffix` to `-lstdc++` |
| 11.4 | u-ca369 | GA7.0 N96 AMIP | fcm:um.xm_br/dev/jeffcole/vn11.4_archer2_fixes |
| 11.5 | u-ca370 | GA7.1 N1280 UM11.5 AMIP | fcm:um.xm_br/dev/jeffcole/vn11.5_archer2_fixes |
| 11.6 | u-bs251/archer2 | GA7.0 N96 UM11.6 AMIP Climate Development (1988 - 2008) | fcm:um.xm_br/dev/jeffcole/vn11.6_archer2_fixes |
| 11.6 | u-cb151 | N96 ORCA025 GC4.0 main assessment run (CMIP6 forcing) | fcm:um.xm_br/dev/jeffcole/vn11.6_archer2_fixes <br><br>`NEMO_LAND_SUPPRESS=false`  |
| 11.7 | u-ca634 | N96 GA8.0 AMIP Climate Development (1988 - 2008) | fcm:um.xm_br/dev/jeffcole/vn11.7_archer2_fixes |
| 11.9 | u-cf362 | N96 ORCA025 GC4.0 UM11.9 | fcm:um.xm_br/dev/jeffcole/vn11.9_archer2_fixes <br><br> No pptransfer app |

*Table 1. Note, for example, u-be303/archer2 indicates the archer2 branch of u-be303.*

### UMUI Jobs

Only UMUI versions 7.3 and 8.4 are supported on ARCHER2.

Note: Only the small executables `pumf` and `cumf` have been built to run on ARCHER2.

CMS have ported 2 standard jobs to ARCHER2:

| UM Version | Job Id | Description |
| ---------- | ------ | ----------- |
| 7.3 | xoxtb | CCMI |
| 8.4 | xoxta | GLOMAP + CLASSIC: RJ4.0 GA4.0 |

See [here]({{ '/archer2/umui' | relative_url }}) for instructions on running and porting UMUI jobs to ARCHER2.
