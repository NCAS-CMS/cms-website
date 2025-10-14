---
layout: page
title: ARCHER2 System Information
subheadline: ARCHER2
permalink: '/archer2/system-info/'
breadcrumb: true
---

### Scheduler:
ARCHER2 uses the [SLURM](https://slurm.schedmd.com/) scheduler.  All batch scripts run on ARCHER will need to be rewritten to work on ARCHER2.  See the ARCHER2 documentation for information on [running jobs on ARCHER2](https://docs.archer2.ac.uk/user-guide/scheduler) and basic slurm commands.

### Login Nodes:
The login nodes currently support the running of persistent ssh-agents enabling data transfer to JASMIN through the Rose/Cylc workflows.

### Compute Nodes:
The compute nodes CANNOT see the `/home` filesystem.  Unlike ARCHER, batch scripts also run on the compute nodes. All files referenced in batch scripts and used by running jobs MUST be located on the `/work` file system.

### Serial/Data Analysis Nodes:
ARCHER2 has 2 data analysis nodes, which are accessible both in batch via the Slurm serial queue and also interactively. See [ARCHER2 Data Analysis documentation](https://docs.archer2.ac.uk/user-guide/analysis/) for full details. This is where the model compilations are run. Due to the configuration of these nodes, it is currently not possible to run ARCHER2 to JASMIN data transfer tasks on the serial nodes.   Whilst the ARCHER2/JASMIN teams work on a permanent solution, data transfers currently need to be run on the login nodes.  Full details on the setup required is available on our [data transfer](https://TODO) page.

### File Systems:
ARCHER2 has a `/home` and `/work` file system with identical structure to that on ARCHER.  We currently have 655TB disk space on `/work` and 4TB on `/home`.  

### Budgets:
The ARCHER2 budget structure and membership works in exactly the same way as for ARCHER2.  See the ARCHER2 documentation for information on [resources and how to check budgets](https://docs.archer2.ac.uk/user-guide/scheduler/#resources).
