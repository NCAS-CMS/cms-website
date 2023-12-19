---
layout: page-fullwidth
subheadline: Cylc 8
title: Cylc 8 on PUMA2 and ARCHER2
---

Cylc 8 is available on PUMA2 and ARCHER2, but is not yet fully supported. 
We are still testing the system, and so the software configuration is subject to change. 
However we encourage you to try it out if you are interested. 
See the links below for further information. 
Report any issues to the helpdesk. 

## Overview 

Cylc 8 replaces the Python 2 based Cylc 7 software. 
It is a complete rewrite in Python 3, and works quite differently from Cylc 7, so we encourage you to look at the documentation. 
The user interface system is still being developed and does not yet have full functionality. 

Useful links: 
* [Cylc 8 documentation](https://cylc.github.io/cylc-doc/stable/html/index.html)
* [Cylc 7 to Cylc 8 migration guide](https://cylc.github.io/cylc-doc/stable/html/7-to-8/index.html)
* [Cylc discourse forum](https://cylc.discourse.group/) 

Note that in Cylc 8 terminology "suites" have become "workflows". 

## Using Cylc 8 on PUMA2 and ARCHER2

Note that we do not yet have any UM workflows available for ARCHER2. 

### Setting the Cylc version 

Set the Cylc version in the terminal: 
```
export CYLC_VERSION=8
```
You should be able to do this alongside any Cylc 7 suites you have running.  
Assuming you have set up your ARCHER2 and Jasmin environments to have Cylc 7 available, 
you should not need to make any further changes. 
The workflow will simply pick up the appropriate Cylc version when it runs. 

### Running a workflow

To run a simple test, copy my workflow ```test.platforms.c8```: 
```
cd ~/roses
cp -r ~annette/roses/test.platforms.c8 . 
```

In the ```test.platforms.c8``` directory, edit the ```rose-suite.conf``` file to set your ARCHER2 username and project code. 

Then run with: 
```
cylc vip 
```

See the [Cylc 8 cheat sheet](https://cylc.github.io/cylc-doc/stable/html/7-to-8/cheat-sheet.html) for an overview of Cylc 8 commands. 

### Platforms 

The ```cylc.flow``` file replaces ```suite.rc```. 
The ```test.platforms.c8``` workflow runs tasks on ARCHER2 and JASMIN in the background and via the Slurm scheduler. 
The way remote tasks are specified is quite different to Cylc 7. 
You specify a "platform" which combines the host and job running method. 
See the [Cylc 8 platform documentation](https://cylc.github.io/cylc-doc/stable/html/reference/config/writing-platform-configs.html#adminguide-platformconfigs) for details. 

On PUMA2 the following platforms are available: 

* PUMA2: 
  * ```localhost``` : background job
* ARCHER2:
  * ```archer2``` : Slurm job 
  * ```archer2_bg``` : background on random login node
  * ```ln0[1-4]_bg``` : background job on specific login node 
* JASMIN:
  * ```lotus``` : Slurm job 
  * ```sci_bg``` : background job on random sci machine
  * ```sci[1-8]_ng``` : background job on specific sci machine

Note that multiplexing is no longer needed to submit jobs to Jasmin. 

There are still sometimes issues if a host is not available, or not fully functional (for example if it can't see the file system or Slurm queue). 

### Using the tui 

### Using the web-based UI with port-forwarding 

### Platforms 




