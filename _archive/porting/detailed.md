---
layout: page-fullwidth
title: Detailed Rose/Cylc Information
subheadline: Porting a UM suite to ARCHER2
permalink: '/archer2/porting/detailed/'
breadcrumb: true
---
## General

The multiplicity and diversity of Rose/Cylc suites prevents us from providing a simple comprehensive guide to suite modifications necessary for running on ARCHER2. However, the [standard suites](https://TODO) that CMS have already ported should give hints on to how to upgrade your suite. The suite changes required stem from the following differences between ARCHER and ARCHER2:

 * **scheduler:** ARCHER uses PBS, ARCHER2 uses SLURM
 * **architecture:** ARCHER has 24 cores per node, ARCHER2 has 128 cores per node 

Changes to account for SLURM will typically be in the `[[directives]]` section of tasks in the `suite.rc` file or in an appropriate `site/archer2.rc` file (you my need to create one of these). The example below serves to illustrate common SLURM features.

**Note:** the SLURM directives `--partition` and `--qos` combine to provide a more flexible replacement for the PBS directive `--queue`. 
{% raw %}
~~~
  [[HPC]]
        pre-script = """
                     ulimit -s unlimited
                     module load um  <====== to load the environment
                     module list 2>&1
                     """

        [[[directives]]]
            --export=none
            --chdir=/work/n02/n02/<your ARCHER2 user name>   <===== you must set this 
            --partition=standard
            --qos={{ARCHER2_QUEUE}}
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
            --partition=serial
            --qos=serial
            --ntasks=1
        [[[job]]]
            execution time limit = PT30M
        [[[environment]]]
            ROSE_TASK_N_JOBS = 1

    [[UMBUILD]]
        [[[environment]]]
            CONFIG = ncas-ex-cce                             <====== note name of config for ARCHER2
            ROSE_TASK_N_JOBS = 32
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

Review one or more of the coupled suites listed in the [Standard Jobs](http://TODO) for a detailed view of changes to the suite needed to run under SLURM.

### moci modules

The moci modules have been rebuilt for use on ARCHER2 to work correctly with MPI threading.

| XIOS revision | OASIS revision | moci module | comment |
| ------------- | -------------- | ----------- | ------- |
| 952 | 2466 | GC3-PrgEnv/2.0/2021.12.15 | Typically used for UKESM suites and older UM version coupled suites |
| 2245 | 2466 | GC3-PrgEnv/2.0/2021.11.22 | |
| 952 | 10f61316 | GC4-PrgEnv/2021.12.1 | Used in GC4.0 suites | 

### SLURM options

SLURM heterogeneous jobs are used for coupled suites where the atmosphere, NEMO, and XIOS are separate executables running under a common communicator. The basic SLURM ideas above carry over to heterogeneous jobs but rather than making an overarching job resource request (as is the case for PBS), the total node count must be specified along with the resource requirements and specifiction for each component of the coupled model.  The SLURM options will typically be applied through the `ROSE_LAUNCHER_PREOPTS_<model_component>` variable, where `<model_component>` is one of UM, NEMO or XIOS.

An example for the UM component:
{% raw %}
~~~
    ROSE_LAUNCHER_PREOPTS_UM = --het-group=0 --nodes={{ATMOS_NODES}} --ntasks={{ATMOS_TASKS}} 
        --tasks-per-node={{ATMOS_PPNU*NUMA}} --cpus-per-task={{OMPTHR_ATM}} --hint=nomultithread 
        --distribution=block:block 
        --export=all,OMP_NUM_THREADS={{OMPTHR_ATM}},HYPERTHREADS={{HYPERTHREADS}},OMP_PLACES=cores
~~~
{% endraw %}

where `--het-group=0 ` is associated with the atmosphere, `--het-group=1` with the ocean, and `--het-group=2` with the (XIOS) io-servers.


