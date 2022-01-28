---
layout: page-fullwidth
title: ARCHER2
teaser: The ARCHER2 service is a world class advanced computing resource for UK researchers. ARCHER2 is provided by <a href="https://www.ukri.org">UKRI</a>, <a href="https://www.epcc.ed.ac.uk">EPCC</a>, <a href="https://www.cray.com"> HPE Cray</a> and the <a href="https://www.ed.ac.uk">University of Edinburgh</a>.
permalink: /archer2/
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

ARCHER2 is an HPE Cray EX supercomputing system with an estimated peak performance of 28 PFLOP/s. The machine has 5,860 compute nodes, each with dual AMD EPYC 7742 64-core CPUs at 2.25GHz, giving 750,080 cores in total. Further details on the [ARCHER2 hardware](https://www.archer2.ac.uk/about/hardware.html) can be found on the [ARCHER2 website](https://www.archer2.ac.uk).

ARCHER users will find the new machine very familiar in many respects but with some important differences - see ​[ARCHER2 YouTube Channel](https://www.youtube.com/channel/UCZi-oBdxoDV5CPEQnhmrCAg/videos) for a comprehensive array of presentations, in particular the one entitled ["Differences between ARCHER and ARCHER2"](https://www.youtube.com/watch?v=dmwGMk9uB-4).

CMS has installed and undertaken limited testing of several versions of the Unified Model and its auxiliary software. We encourage users where possible to migrate their workflows to use the latest versions of the UM.

## System Information

**Scheduler:** \\
ARCHER2 uses the [SLURM](https://slurm.schedmd.com/) scheduler.  All batch scripts run on ARCHER will need to be rewritten to work on ARCHER2.  See the ARCHER2 documentation for information on [running jobs on ARCHER2](https://docs.archer2.ac.uk/user-guide/scheduler) and basic slurm commands.

**Login Nodes:** \\
The login nodes currently support the running of persistent ssh-agents enabling data transfer to JASMIN through the Rose/Cylc workflows.

**Compute Nodes:** \\
The compute nodes CANNOT see the `/home` filesystem.  Unlike ARCHER, batch scripts also run on the compute nodes. All files referenced in batch scripts and used by running jobs MUST be located on the `/work` file system.

**Serial/Data Analysis Nodes:** \\
ARCHER2 has 2 data analysis nodes, which are accessible both in batch via the Slurm serial queue and also interactively. See [ARCHER2 Data Analysis documentation](https://docs.archer2.ac.uk/user-guide/analysis/) for full details. This is where the model compilations are run. Due to the configuration of these nodes, it is currently not possible to run ARCHER2 to JASMIN data transfer tasks on the serial nodes.   Whilst the ARCHER2/JASMIN teams work on a permanent solution, data transfers currently need to be run on the login nodes.  Full details on the setup required is available on our [data transfer](https://TODO) page.

**File Systems:** \\
ARCHER2 has a `/home` and `/work` file system with identical structure to that on ARCHER.  We currently have 655TB disk space on `/work` and 4TB on `/home`.  

**Budgets:** \\
The ARCHER2 budget structure and membership works in exactly the same way as for ARCHER2.  See the ARCHER2 documentation for information on [resources and how to check budgets](https://docs.archer2.ac.uk/user-guide/scheduler/#resources).

## Getting an account on ARCHER2

To apply for an n02 project account please follow the instructions for [requesting an ARCHER2 login account](https://docs.archer2.ac.uk/quick-start/quickstart-users/#request-an-account-on-archer2). 

## Unified Model on ARCHER2

CMS have installed the following versions of the UM on ARCHER2: 7.3, 8.4, 10.7, 11.1+, 12.x

### Getting Started

Several setup steps are required before running the UM for the first time on ARCHER2:

For those that have never run the UM before:
* Register for an ARCHER2 account. ([See above](#getting-an-account-on-archer2))
* Register for a PUMA account by contacting the [CMS Team]({{ '/contact/' | relative_url}}).
* Setup your PUMA and ARCHER2 environments by following the [set up instructions](https://ncas-cms.github.io/um-training/getting-setup.html#set-up-your-archer2-environment) in our online training.

For those that have previously run the UM on ARCHER:
* Register for an ARCHER2 account. ([See above](#getting-an-account-on-archer2))
* Setup your ARCHER2 environment. Ensure you have the following line in your `~/.bash_profile` on ARCHER2: \\
  `. /work/y07/shared/umshared/bin/rose-um-env` \\
  **Note:** the path change from ARCHER.

### UMDIR (umshared)

All UM data and software is installed centrally under `/work/y07/shared/umshared`.

UKCA input files that used to be under `/work/n02/n02/ukca` on ARCHER now reside under `$UMDIR/ukca`.

Users may set `UMDIR` in their `~/.bash_profile` but remember that batch jobs can't see `/home` and therefore will not source any scripts that reside there.

### Standard Suites

CMS maintain a number of standard suite configuations on ARCHER2. All standard suites available are detailed on the [UM Configurations]({{ '/unified-model/configurations' | relative_url }}) page.

### Porting from ARCHER to ARCHER2

See the [porting page]({{ '/archer2/porting/' | relative_url }}) for instructions on how to port a UM suite or UMUI job to ARCHER2. Example suites that CMS have already ported can also be found on this page.

### Performance

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

