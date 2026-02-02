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

## Overview 

Cylc 8 replaces the Python 2 based Cylc 7 software. 
It is a complete rewrite in Python 3 and contains many changes from Cylc 7, so we encourage you to look at the documentation. 

Useful links: 
* [Cylc 8 documentation](https://cylc.github.io/cylc-doc/stable/html/index.html)
* [Cylc 8 cheat sheet](https://cylc.github.io/cylc-doc/stable/html/user-guide/cheat-sheet.html)
* [Cylc discourse forum](https://cylc.discourse.group/)
  
* [Cylc 7 to Cylc 8 migration guide](https://cylc.github.io/cylc-doc/stable/html/7-to-8/index.html)
* [Cylc 7 to Cylc 8 cheat sheet](https://cylc.github.io/cylc-doc/stable/html/7-to-8/cheat-sheet.html)

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

## ARCHER2 workflows

Cylc-8 workflows available on ARCHER2: 

| Cylc 8 id | Cylc 7 id | UM version | Description | 
| :--- | :--- | :--- | :--- |
| u-dj397 | u-cc519 | 13.0 | N48 GA6 (training suite) | 
| u-da412/archer2 | -   | 13.5 | GC5-UM      |

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

See the [Cylc 8 cheat sheet](https://cylc.github.io/cylc-doc/stable/html/user-guide/cheat-sheet.html) for an overview of Cylc 8 commands. 

## Platforms 

Tasks are assigned a "platform", which combines the host and job running method. 
See the [Cylc 8 platform documentation](https://cylc.github.io/cylc-doc/stable/html/reference/config/writing-platform-configs.html#adminguide-platformconfigs) for details. 

On PUMA2 the following platforms are available: 

* PUMA2: 
  * ```localhost``` : background job
* ARCHER2:
  * ```archer2``` : Slurm job 
  * ```archer2-bg``` : background on random login node
  * ```ln0[1-4]``` : background job on specific login node
* ARCHER2 with the `cylc-run/runN/` `share/` and `work/` directories symlinked to the NVMe file system:
  * ```archer2-nvme``` : Slurm job 
  * ```archer2-nvme-bg``` : background on random login node
  * ```ln0[1-4]-nvme``` : background job on specific login node 
* JASMIN:
  * ```lotus2``` : Slurm job on [lotus2 cluster](https://help.jasmin.ac.uk/docs/software-on-jasmin/rocky9-migration-2024/#upgraded-lotus-cluster)
  * ```sci-vm``` : background job on random [scientific analysis server](https://help.jasmin.ac.uk/docs/interactive-computing/sci-servers/)
  * ```sci-vm-0[1-6]``` : background job on specific sci server

Jasmin notes: 
* Multiplexing is no longer needed to submit jobs to Jasmin. 
* You will need to configure your ssh config file to be able to access the sci servers from puma2.

You can test submission to each of the platforms with the workflow u-dj398.

## Using the Cylc web UI

### Setup

The web-based Cylc UI is available via port-forwarding which requires some setup. 
Here we provide instructions for Linux, Mac & MobaXterm (Windows).

Edit the ```~/.ssh/config``` file on your laptop so that the ARCHER2 and PUMA2 sections contain:

```
# PUMA2
Host puma2
User <username>
IdentityFile ~/.ssh/<your-archer-ssh-key>
ProxyJump archer2

# ARCHER2
Host archer2
Hostname login.archer2.ac.uk
User <username>
IdentityFile ~/.ssh/<your-archer-ssh-key>
ForwardX11 No
ControlMaster auto
ControlPath /tmp/ssh-socket-%r@%h-%p
ControlPersist yes
```

You should now be able to type ```ssh puma2``` and land directly on PUMA2.

Setup an alias on your laptop by adding one for the following to your ```~/.bashrc``` or equivalent depending on whether you are using Linux or a Mac.

#### Linux 

```
alias puma-ui='PORT=$(shuf -n 1 -i 10000-65000); ssh -t -L ${PORT}:localhost:${PORT} puma2 "bash -l -c \"export CYLC_VERSION=8; cylc gui --no-browser --Application.log_level=WARN --port-retries=0 --port=${PORT}\""'
```

#### Mac

```
alias puma-ui='PORT=$(jot -r 1 10000 65000); ssh -t -L ${PORT}:localhost:${PORT} puma2 "bash -l -c \"export CYLC_VERSION=8; cylc gui --no-browser --Application.log_level=WARN --port-retries=0 --port=${PORT}\""'
```

#### Windows

```
alias puma-ui='PORT=$(shuf -n 1 -i 10000-65000); ssh -t -L ${PORT}:localhost:${PORT} puma2 "bash -l -c \"export CYLC_VERSION=8; cylc gui --no-browser --Application.log_level=WARN --port-retries=0 --port=${PORT}\""'
```

### Start up the cylc web GUI

In a new terminal window type: ```puma-ui``` 

You will see a response similar to the following:

```
$ puma-ui
#################################################################################
------------------------------Welcome to PUMA2-----------------------------------
#################################################################################
[C 2026-01-22 08:25:30.367 ServerApp]
To access the server, open this file in a browser:
(continues on next page)
8
NCAS Unified Model Introduction: Practical sessions (Rose/Cylc)
(continued from previous page)
file:///home/n02/n02/ros/.cylc/uiserver/info_files/jpserver-1094362-open.html
Or copy and paste one of these URLs:
http://localhost:20522/cylc?
˓→token=700ab2be96800177d03df31b8140857cab02b9632af45a1d
http://127.0.0.1:20522/cylc?
˓→token=700ab2be96800177d03df31b8140857cab02b9632af45a1d
[W 2026-01-22 08:25:44.242 ServerApp] The websocket_ping_timeout (999999) cannot␣
˓→be longer than the websocket_ping_interval (290).
Setting websocket_ping_timeout=290
```

Copy and paste one of the http URLs listed into your web browser and you should then see your Cylc GUI
load. If you have never used Cylc8 before the Workflows panel will be empty.

