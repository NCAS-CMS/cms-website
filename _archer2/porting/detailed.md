---
layout: page-fullwidth
title: Detailed Rose/Cylc Information
subheadline: Porting a UM suite to ARCHER2
permalink: '/archer2/porting/detailed'
breadcrumb: true
---
## General

The multiplicity and diversity of Rose/Cylc suites prevents us from providing a simple comprehensive guide to suite modifications necessary for running on ARCHER2. However, the standard suites that CMS have already ported should give hints on to how to upgrade your suite. The suite changes required stem from the following differences between ARCHER and ARCHER2:

 * scheduler: ARCHER uses PBS, ARCHER2 uses SLURM
 * architecture: ARCHER has 24 cores per node, ARCHER2 has 128 cores per node 

Changes to account for SLURM will typically be in the `[[directives]]` section of tasks in the `suite.rc` file or in an appropriate `site/archer2.rc` file (you my need to create one of these.) The example below serves to illustrate common SLURM features.

**Note:** the SLURM directives `--partition`, `--qos`, and `--reservation` combine to provide a more flexible replacement for the PBS directive `--queue`. Additional partitions will become available with the full ARCHER2 system.
{% raw %}
~~~
  [[HPC]]
        pre-script = """
                     ulimit -s unlimited
                     TOMP_NUM_THREADS=${OMP_NUM_THREADS:-}
                     module restore $UMDIR/modulefiles/um/2020.12.14  <====== to load the environment
                     module list 2>&1
                     export OMP_NUM_THREADS=$TOMP_NUM_THREADS
                     """


        [[[directives]]]
            --export=none
            --chdir=/work/n02/n02/<your ARCHER2 user name>   <===== you must set this 
            --partition=standard
            --qos={{ARCHER2_QUEUE}}
{% if ARCHER2_QUEUE == 'short' %}
            --reservation=shortqos
{% endif %}
            --account={{ARCHER2_GROUP}}
        [[[environment]]]
            PLATFORM = cce
            UMDIR = /work/y07/shared/umshared
        [[[job]]]
            batch system = slurm                             <===== specify use of SLURM
        [[[remote]]]
            host = login.archer2.ac.uk                       <====== use ARCHER2
{% if HPC_USER is defined %}
            owner = {{HPC_USER}}
{% endif %}

    [[HPC_SERIAL]]
        inherit = HPC
        [[[directives]]]
            --nodes=1
            --tasks-per-node=128
            --cpus-per-task=1
        [[[environment]]]
            ROSE_TASK_N_JOBS = 32

    [[UMBUILD]]
        [[[environment]]]
            CONFIG = ncas-ex-cce                             <====== note name of config for ARCHER2
~~~
{% endraw %}         

Setting SLURM options that specify the number of processors requires assigning values to `--nodes`, `--ntasks`, `--tasks-per-node`, and `--cpus-per-task`. These should be familiar from ARCHER modulo the precise names for the attributes. Your suite may use different names for the various parameters, such as `TASKS_RCF`, for example, but there should be a simple correspondence.
{% raw %}
~~~
   [[RCF_RESOURCE]]
        inherit = UM_PARALLEL
        [[[directives]]]
            --nodes={{NODE_RCF}}
            --ntasks= {{TASKS_RCF}}
            --tasks-per-node={{8*(TPNUMA_RCF|int)}}
            --cpus-per-task={{MAIN_OMPTHR_RCF}}
        [[[environment]]]
            OMP_NUM_THREADS={{MAIN_OMPTHR_RCF}}
            ROSE_LAUNCHER_PREOPTS = {{RCF_SLURM_FLAGS}}
        [[[job]]]
            execution time limit = PT20M

    [[ATMOS_RESOURCE]]
        inherit = UM_PARALLEL, SUBMIT_RETRIES
        [[[directives]]]
            --nodes={{NODE_ATM}}
            --ntasks= {{TASKS_ATM}}
            --tasks-per-node={{8*(TPNUMA_ATM|int)}}
            --cpus-per-task={{MAIN_OMPTHR_ATM}}
        [[[environment]]]
            OMP_NUM_THREADS={{MAIN_OMPTHR_ATM}}
            ROSE_LAUNCHER_PREOPTS = {{ATM_SLURM_FLAGS}}
        [[[job]]]
            execution time limit = {{MAIN_CLOCK}}
~~~
{% endraw %}

Your suite should include a section to specify the flags that will be passed the command to launch the job (for ARCHER that command is `aprun`, for ARCHER2 it is `srun`.) The flags are different for jobs running with or without OpenMP. Most suites will need some Jinja like this:
{% raw %}
~~~
{# set up slurm flags for OpenMP/non-OpenMP #}
{% if MAIN_OMPTHR_RCF > 1 %}
  {% set RCF_SLURM_FLAGS= "--hint=nomultithread --distribution=block:block" %}
{% else %}
  {% set RCF_SLURM_FLAGS = "--cpu-bind=cores" %}
{% endif %}
{% if MAIN_OMPTHR_ATM > 1 %}
  {% set ATM_SLURM_FLAGS= "--hint=nomultithread --distribution=block:block" %}
{% else %}
  {% set ATM_SLURM_FLAGS = "--cpu-bind=cores" %}
{% endif %}
~~~
{% endraw %}
Suites frequently contain macros to calculate the number of nodes and cores required - the only change needed is to set to 8 the number of NUMA regions per node.

## Coupled suites

Review one or more of the coupled suites listed in the Standard Jobs page for a detailed view of changes to the suite needed to run under SLURM.

We have adopted the SLURM heterogeneous jobs method of handling coupled suites where the atmosphere, NEMO, and XIOS are separate executables running under a common communicator. The basic SLURM ideas above carry over to heterogeneous jobs but rather than making an overarching job resource request (as is the case for PBS), each component of the coupled job specifies its own requirements.

For the coupled task (or in its inherited resources)
{% raw %}
~~~
    [[[directives]]]
        hetjob_0_--nodes={{ATMOS_NODES}}
        hetjob_0_--ntasks={{ATMOS_TASKS}}
        hetjob_0_--tasks-per-node={{ATMOS_PPNU*NUMA}}
        hetjob_0_--cpus-per-task={{OMPTHR_ATM}}
        hetjob_1_--partition=standard
        hetjob_1_--nodes={{OCEAN_NODES}}
        hetjob_1_--ntasks= {{OCEAN_TASKS}}
        hetjob_1_--tasks-per-node={{OCEAN_PPNU*NUMA}}
        hetjob_1_--cpus-per-task={{OMPTHR_OCN}}
        hetjob_2_--partition=standard
        hetjob_2_--nodes={{XIOS_NODES}}
        hetjob_2_--ntasks= {{XIOS_TASKS}}
        hetjob_2_--tasks-per-node={{XIOS_PPNU*NUMA}}
        hetjob_2_--cpus-per-task=1
~~~
{% endraw %}

where `hetjob_0_` is associated with the atmosphere, `hetjob_1_` with the ocean, and `hetjob_2_` with the (XIOS)io-servers.

The variables `ROSE_LAUNCHER_PREOPTS_UM`, `ROSE_LAUNCHER_PREOPTS_NEMO`, and `ROSE_LAUNCHER_PREOPTS_XIOS` also need modification to link the resource request to the job launcher command, for example:

{% raw %}
~~~
    {% if OMPTHR_ATM > 1 %}
      ROSE_LAUNCHER_PREOPTS_UM  = --het-group=0 --hint=nomultithread --distribution=block:block --export=all,OMP_NUM_THREADS={{OMPTHR_ATM}},HYPERTHREADS={{HYPERTHREADS}},OMP_PLACES=cores
    {% else %}
      ROSE_LAUNCHER_PREOPTS_UM  = --het-group=0 --cpu-bind=cores --export=all,OMP_NUM_THREADS={{OMPTHR_ATM}},HYPERTHREADS={{HYPERTHREADS}}
    {% endif %}
~~~
{% endraw %}
where the flag `--het-group=0` makes the connection to `hetjob_0_`. 