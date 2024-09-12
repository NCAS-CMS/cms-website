---
layout: page-fullwidth
subheadline: Cylc 8
title: Cylc 8 on PUMA2 and ARCHER2
permalink: /cylc8/
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

***Cylc 8 is available on PUMA2 and ARCHER2, but has not yet been widely used.  
We are still testing the system, and so the software configuration is subject to change.***

See the links below for further information. 
Report any issues to the helpdesk. 

## Overview 

Cylc 8 replaces the Python 2 based Cylc 7 software. 
It is a complete rewrite in Python 3 and contains many changes from Cylc 7, so we encourage you to look at the documentation. 
The user interface system is still being developed and does not yet have full functionality. 

Useful links: 
* [Cylc 8 documentation](https://cylc.github.io/cylc-doc/stable/html/index.html)
* [Cylc 7 to Cylc 8 migration guide](https://cylc.github.io/cylc-doc/stable/html/7-to-8/index.html)
* [Cylc 8 cheat sheet](https://cylc.github.io/cylc-doc/stable/html/7-to-8/cheat-sheet.html)
* [Cylc discourse forum](https://cylc.discourse.group/) 

Note that in Cylc 8 terminology "suites" have become "workflows". 

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

## ARCHER2 workflows

Cylc-8 workflows available on ARCHER2: 

| Cylc 8 id | Cylc 7 id | Description | 
| :--- | :--- | :--- |
| u-de385 | u-cy010   | GC5-UM      |
| u-dj397 | u-cc519 | N48 GA6 (training suite) | 

See the [instructions for migrating an ARCHER2 Cylc 7 suite to Cylc 8](upgrading-workflows/). 

## Using Cylc 8 on PUMA2 and ARCHER2

### Setting the Cylc version 

Set the Cylc version in the terminal: 
```
export CYLC_VERSION=8
```
You should be able to do this alongside any Cylc 7 suites you have running.  

Assuming you have set up your ARCHER2 environment (and JASMIN if required) to have Cylc 7 available, 
you should not need to make any further changes. 
The workflow will simply pick up the appropriate Cylc version when it runs. 

### Running a workflow

To run a simple test, checkout u-dj397
```
rosie co u-dj397
```
Set your username and project account in `rose-suite.conf` or in the GUI via `rose edit`. 

Run the workflow with: 
```
cylc vip 
```

Launch the terminal user interface to check on progress: 
```
cylc tui u-dj397
```

See the [Cylc 8 cheat sheet](https://cylc.github.io/cylc-doc/stable/html/7-to-8/cheat-sheet.html) for an overview of Cylc 8 commands. 

## Further information

### Platforms 

Tasks are assigned a "platform", which combines the host and job running method. 
See the [Cylc 8 platform documentation](https://cylc.github.io/cylc-doc/stable/html/reference/config/writing-platform-configs.html#adminguide-platformconfigs) for details. 

On PUMA2 the following platforms are available: 

* PUMA2: 
  * ```localhost``` : background job
* ARCHER2:
  * ```archer2``` : Slurm job 
  * ```archer2_bg``` : background on random login node
  * ```ln0[1-4]``` : background job on specific login node
* ARCHER2 with the `cylc-run/runN/` `share/` and `work/` directories symlinked to the NVMe file system:
  * ```archer2_nvme``` : Slurm job 
  * ```archer2_nvme_bg``` : background on random login node
  * ```ln0[1-4]_nvme``` : background job on specific login node 
* JASMIN:
  * ```lotus``` : Slurm job 
  * ```sci_bg``` : background job on random sci machine
  * ```sci[1-8]``` : background job on specific sci machine

Note that multiplexing is no longer needed to submit jobs to Jasmin. There are still some issues if a host is not available or not fully functional. We have not yet set up support for the new Jasmin servers. 

You can test submission to each of the platforms with the workflow u-dj398.

### Using the web-based UI with port-forwarding 

Copying the instructions documented [here](https://cylc.discourse.group/t/unclear-on-how-cylc-8-components-work-together/787/2)

> First open an ssh tunnel, so that a given port on your local machine (e.g. your laptop) maps to the Cylc UI Server’s port on the HPC. On your local machine, type
> ```
> $ ssh -N -L PORT:localhost:PORT HOST
> ```
> where PORT is a valid port number and HOST is on the HPC. You will need to know the range of allowed ports (e.g.1024-49151). Choose any number in this range but make sure your port number is fairly unique to avoid clashing with other users. (Note the option -N opens the connection without logging you into the shell).
> 
> Then ssh to the host:
> ```
> $ ssh HOST
> ```
> and add the following to $HOME/.cylc/uiserver/jupyter_config.py on the HOST.
> ```
> c.ServerApp.open_browser=False
> c.ServerApp.port=PORT
> ```
> where PORT and HOST match the values you selected when opening the ssh tunnel.
>
> You’re now ready to fire up the web graphical interface
> ```
> $ cylc gui
> ```
> Just copy the URL that looks like
> ```
> http://127.0.0.1:PORT/cylc?token=TOKEN
> ```
> into your web browser. (Again substitute HOST and PORT with the values chosen above.)

Note that each user needs a unique port number. 
