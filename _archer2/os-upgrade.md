---
layout: page-fullwidth
title: ARCHER2 O/S Upgrade
subheadline: Updating a UM suite after the ARCHER2 O/S upgrade 
permalink: '/archer2/os-upgrade/'
breadcrumb: true
---

<font color="red"><b>!! This page is under construction !!</b></font>

In May/June 2023, Archer2 underwent a [major software upgrade](https://docs.archer2.ac.uk/faq/upgrade-2023/). All the system software, including compilers and libraries were updated, and as a result, we have had to rebuild much of the UM supporting software. This means users need to make some changes to their suites and test their workflows before resuming work. 

We have ported and tested some of the commonly-used suites, listed below. And we have provided a guide to the suite changes required. As ever, since UM suites can be set up in so many different ways, we can not provide a comprehensive set of instructions. Please get in touch with the [helpdesk](https://cms-helpdesk.ncas.ac.uk/) if you run into diffculties. 

## Instructions 

### Atmosphere
For atmosphere-only suites that use standard build configurations, user-level changes are not required and such suites should run successfully once the UM executables for the reconfigurarion and the atmosphere model have been rebuilt.

### Coupled
Coupled atmosphere-ocean suites do require some user level changes to suite files.
1. Change the Science Configuration Module (see the table below for the required mappings)
2. Update the cce module version and remove the ucx module swap entries in archer2.rc, ie, change
    ```
     module load cce/12.0.0
     module swap craype-network-ofi craype-network-ucx
     module swap cray-mpich cray-mpich-ucx/8.1.15
    {{MODULE_CMD}}
    ```
to

 ```
    module load cce/15.0.0
    {{MODULE_CMD}}
 ```
## Ported suites 

| UM version | Suite id | Description | Branches + Notes |

| 11.1 | u-be303 | UKESM1.0 AMIP |  |
| 11.2 | u-bc613 | UKESM1.0 Historical | see changes to the hetjob config in site/archer2.rc |
| 11.2 | u-bc994 | UKESM1.0 pre-industrial control | see changes to the hetjob config in site/archer2.rc |


## How to restart suites that were running at the time ARCHER2 went down
