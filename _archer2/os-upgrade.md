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

The following instructions draw on the naming style typically found in climate suites, but the ideas should apply to all UM suites. Suite modifications derive to accommodate changes to the slurm job scheduler. Minimal user-level changes are required and suites should run successfully once the UM executables for the reconfigurarion and the atmosphere model have been rebuilt.

### Atmosphere
For atmosphere-only suites add the ```--cpus-per-task={{MAIN_OMPTHR_ATM}}``` clause to the atmopshere resources ```[[[environment]]]``` section in ```archer2.rc```:
```
[[ATMOS_RESOURCE]]
...
      [[[environment]]]
            OMP_NUM_THREADS={{MAIN_OMPTHR_ATM}}
            ROSE_LAUNCHER_PREOPTS = {{ATM_SLURM_FLAGS}} --cpus-per-task={{MAIN_OMPTHR_ATM}}
```

### Coupled
Coupled atmosphere-ocean suites require changes to suite files ```rose-suite.conf``` and ```archer2.rc```.
1. In ```rose-suite.conf``` change the Science Configuration Module (see the table below for the required mappings)
2. Update the cce module version and remove the ucx module swap entries in ```archer2.rc```, ie, change
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

3. Update the ```ROSE_LAUNCHER_PREOPTS``` for the UM, NEMO, and XIOS. There is no longer any need to distinguish singly and multithreaded cases, but note the clauses ``` --hint=nomultithread --distribution=block:block``` must appear in the ```ROSE_LAUNCHER_PREOPTS``` for the UM, NEMO, and XIOS.

```html
       [[UM_RESOURCE]]
           [[[environment]]]
                  ROSE_LAUNCHER_PREOPTS_UM  = --het-group=0 --nodes={{ATMOS_NODES}} --ntasks={{ATMOS_TASKS}} --tasks-per-node={{ATMOS_PPNU*NUMA}} --cpus-per-task={{OMPTHR_ATM}} --hint=nomultithread --distribution=block:block --export=all,OMP_NUM_THREADS={{OMPTHR_ATM}},HYPERTHREADS={{HYPERTHREADS}},OMP_PLACES=cores
    
       [[NEMO_RESOURCE]]
             [[[environment]]]
                  ROSE_LAUNCHER_PREOPTS_NEMO  = --het-group=1 --nodes={{OCEAN_NODES}} --ntasks={{OCEAN_TASKS}} --tasks-per-node={{OCEAN_PPNU*NUMA}} --cpus-per-task={{OMPTHR_OCN}} --hint=nomultithread --distribution=block:block --export=all,OMP_NUM_THREADS={{OMPTHR_OCN}},HYPERTHREADS={{HYPERTHREADS}},OMP_PLACES=cores
    
                  {%   if XIOS_NPROC is defined and XIOS_NPROC > 0 %}
                  ROSE_LAUNCHER_PREOPTS_XIOS  = --het-group=2 --nodes={{XIOS_NODES}} --ntasks={{XIOS_TASKS}} --tasks-per-node={{XIOS_PPNU*NUMA}} --cpus-per-task=1 --hint=nomultithread --distribution=block:block --export=all,OMP_NUM_THREADS=1,HYPERTHREADS=1
```


## Ported suites 

UM version | Suite id | Description | Branches + Notes
:---------:|:--------:|:-----------:|:----------------:
11.1 | u-be303 | UKESM1.0 AMIP | n/a
11.2 | u-bc613 | UKESM1.0 Historical | see changes to the hetjob config in site/archer2.rc
11.2 | u-bc994 | UKESM1.0 pre-industrial control | see changes to the hetjob config in site/archer2.rc
11.6 | u-bs251 | GA7.0 N96 AMIP Climate Development | n/a


## How to restart suites that were running at the time ARCHER2 went down
