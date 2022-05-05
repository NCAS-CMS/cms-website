---
layout: page-fullwidth
title: Standalone UM system and FAMOUS
subheadline: Miscellaneous
teaser: This is a standalone version of FAMOUS based on version 4.5 of the Met Office's Unified Model (UM).
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

The current version is 1.1.0. It is available at github [https://github.com/NCAS-CMS/FAMOUS](https://github.com/NCAS-CMS/FAMOUS)

Two standard FAMOUS versions are supplied, one with the MOSESI land-surface scheme, and the other with MOSESII.2. The base runids for these configurations are xhmkq and xfhcr (under robin) respectively.

It has a complete UM system but without the need for the complicated installation process.
It is linux only as it comes with pre-built small  executables.
It also comes with prebuilt model and reconfiguration executables.
If no model code changes are needed, then the model executables can be used for model integration without the need for any compilation at all on the installation machine.

As the executables are statically linked, they will run on any modern linux machine.

The system has the flexibility for local compilation, if required.
This does need extra work, however. The communications library, gcom will need installing, together with a MPI system, see below for full details.

All of the standard FAMOUS input ancillaries are supplied, together with initial dumps.

The UM and FAMOUS can be installed on any linux system, from laptops to clusters. Currently the only job control software supported is the at daemon and slurm (with provios, see below). It is possible to run with other job control systems such as Sun Grid Engine, and an experiment system for this functionality is included.

umui configurations are available for both MOSESI and MOSESII. These have been simplified as much as possible with the mods and handedits concatenated and superfluous options removed.

The package tarball is located at: `/net/jasmin/users/simon/um_famous1.0.2.tgz` 


This document assumes the user is familiar with the UM and UMUI.

## Prerequisites:

* **Running without compilation:**
  * Linux system
  * at daemon
  * ksh
  * A puma.nerc.ac.uk account

  (`at` and `ksh` may not be installed by default)

* **Running with compilation (above plus):**
  * Intel fortran
  * A MPI implementation with mpif77/mpif90

</div><!-- /.medium-8 -->
</div><!-- /.row -->

## Quick start guide:

1. Either down load from github (recommended)
~~~
mkdir /path/to/install/location
cd /path/to/install/location
git clone https://github.com/NCAS-CMS/FAMOUS
~~~
 or copy `/net/jasmin/users/simon/um_famousx.x.x.tgz` and unpack on the machine on which you want to run FAMOUS. The system will be unpacked into a directory called um_famous

2. Edit example.profile to change the values of `UMDIR` and `DATA_DIR`, and append to your `$HOME/.profile`. `UMDIR` should end with um_famous directory if using the tarball, or directory from where the git clone command was run. (If `$HOME/.profile` doesn't exist, try looking for `$HOME/.bash_profile` and use that instead). Ensure that there is no other UM setup commands in `.profile`

3. Then
~~~
. $HOME/.profile
~~~
 If you have used the git repository, then
~~~
gunzip -v $UMDIR/data/dumps/*
~~~

4. Then type:
~~~
umsubmit_local -u pumauserid xmjne
~~~
 for a MOSESI job or
~~~
umsubmit_local -u pumauserid xmjnf
~~~
 for a MOSESII job. You may be asked for your PUMA password. As prebuilt executables are provided, there is no need to build the model. For testing, these model configs require no changes.

5. And the model should be running. Check by:
~~~
cd $DATA_DIR/runid
tail -f *pe0
~~~
 where runid is the 5 letter run ID (xmjne or xmjnf in these cases.)


6. Optional. On puma, you can copy the job xmjne (MOSESI) or xmjnf (MOSESII) from user simon first, then, save and process. The "Submit" button '''DOES NOT WORK'''. Use the umsubmit_local command above to submit the jobs.

## Using slurm

FAMOUS normally runs with the "at" daemon for job control. It is possible to run FAMOUS using the slurm job control systems normally found on clusters and supercomputers. However it will only work for those clusters in which slurm has been configured to use a MPICH derived MPI (MPICH, Cray MPT, Intel MPI, MVAPICH). Also note that it'll only work on the single node.

### Slurm and containerisation

FAMOUS can use slurm and a Singularity container. Please see the ARCHER2 guide below for details.

### To set up slurm

1. Copy a working FAMOUS job in the umui.

2. Go to `Submodel Independent->Job submission, resources and re-submission pattern` window and select `slurm`

3. Set the job time limit to something suitable (this will be based on any slurm queue time limit of the target machine). This '''HAS''' to be in `hh:mm:ss` format.

4. Add a path to a file containing any extra slurm configuration required to set the required slurm queue and account information. Example are `$UMDIR/slurm/racc.slurm` which is configured for the Reading RACC system (and is actually empty). A more general example is `$UMDIR/slurm/example.slurm`:
~~~
#Account info
#SBATCH --account=n02
#Queue info
#SBATCH --partition=standard
#SBATCH --qos=standard
~~~
 Which sets the account and has the required options to run in the `standard` queue on the target machine. The target machine's documentation will indicate what these should be. \\
 Use `$UMDIR/slurm/dummy.slurm` if no extra slurm options are needed.

5. Process and submit as usual. Resubmission using the slurm queues should work.

## ARCHER2

Portable FAMOUS works on ARCHER2 using slurm. There are some issues:
* `$HOME` is unavailable within the slurm environment. `umui_runs` was assumed to be under `$HOME`, but now there is a `UMUI_RUNS` environment variable which overrides this, if set,
* The Intel compiler isn't available. However, a containerised version of the latest release is. The model can be compiled using this containerised version of the compiler and `MPICH`, and then run using ARCHER2's `MPI` libraries by amking use of MPICH ABI. See [https://www.mpich.org/abi/](https://www.mpich.org/abi/)
* The pre-compiler model executables will not work. However, the pre-compiled recon executable will.

All input and output files have to be on the `\work` area.

### Quickstart 

This uses a existing FAMOUS installation under `/work/n02/n02/simon/FAMOUS`

1. On ARCHER2 edit `~/.bash_profile` and add:
~~~
export DATA_DIR=${DATA_DIR:-/work/n02/n02/${USER}}
export UMDIR=/work/n02/n02/simon/FAMOUS
export UMUI_RUNS=$DATA_DIR
. $UMDIR/setvars_4.5
~~~
 Here the `UMUI_RUNS` environment is set to `DATA_DIR`. Note: You will be unable to run centrally installed versions of the UM when these lines are in `~/.bash_profile`.

2. On PUMA start the umui and copy a working portable FAMOUS job, such as `xmjnf` under user `simon`.
 Open the copied job and:
 * In the `Job submission` window select `slurm`, set the job time limit (max 24 hours) and set `$UMDIR/slurm/archer2.slurm` as slurm file
 * In the `Compile options for model` window. Select `Compile and build`, set the time limit to `20`, set the directory to `$DATAW` and the filename to `$RUNID.exe`
 * Copy user mods to ARCHER2 under `\work` and update paths in umui.
 * Save and process
 * Now use `umsubmit_local` on ACRHER2 to build executable.
 * The model should now be built and ready to run.

3. Copy over required input data and update paths in umui. Run using `umsubmit_local`

### Installation and use of FAMOUS on ARCHER2 
These instructions uses the quick start guide above and a basis.
1. Clone the latest version of FAMOUS. Note: '''This has to be cloned under `/work`'''
~~~
git clone https://github.com/NCAS-CMS/FAMOUS
~~~
2. Update `~/.bash_profile` to use installed FAMOUS \\
 Add:
~~~
export DATA_DIR=${DATA_DIR:-${WORKDIR}}
export UMDIR=/path/to/FAMOUS
export UMUI_RUNS=$DATA_DIR
. $UMDIR/setvars_4.5
~~~
 Here the `UMUI_RUNS` environments is set to `DATA_DIR`. Note: You will be unable to run centrally installed versions of the UM when these lines are in `~/.bash_profile`.

3. Then
~~~
. $HOME/.bash_profile
gunzip -v $UMDIR/data/dumps/*
~~~

4. Edit `$UMDIR/slurm/acrher2.slurm`. This file contains the local ARCHER2 configuration. Some notes on ths file. Sections in bold need editing:
 * Change '''`#SBATCH --account=<your account>`''' to the required ACRHER2 account.
 * As `~/.bash_profile` is unavailable when running in batch, the UM config need to be repeated. Set '''`UMDIR`''' and '''`DATA_DIR`''' to their locations.
 * The singularity container is installed on ARCHER2, alternatively a prebuilt version  can be downloaded. See file for details.
 * `MPIF90_UM` overrides the default `mpif90` command if set. The Intel compiler is containerised in `$SINGULARITY_CONTAINER`. By using
~~~
export MPIF90_UM="singularity exec -B /work/n02/n02,/opt/cray,/usr/lib64:/usr/lib/host $SINGULARITY_CONTAINER /container/mpich/bin/mpif90"
~~~
 the containerised version of the compiler is used for all compilation.
 * A shared executable is required to make use of Cray's MPI librbaies. `export MPIF90_SHARED=1` sets this.
 * `LD_LIBRARY_PATH` is updated to use the local Cray MPI libraries


5. Build gcom
 * source `archer2.slurm` to set up compiler.
~~~
. $UMDIR/slurm/archer2.slurm
~~~
 * cd into gcom dir and build
~~~
cd $UMDIR/gcom3.8/gcom
make
~~~
 This should build gcom using the containerised Intel compiler. Ignore any warning messages of the form `Bind mount '/work/n02/n02 => /work/n02/n02' overlaps container CWD /work/n02/n02/simon/test/FAMOUS/gcom3.8/gcom/src/gcom/gcg, may not be available`
 * `$UMDIR/gcom3.8/gcom/lib/libgcom_buffered_mpi.a` should now exist.

6. Then follow steps 2. and 3. in the quickstart guide above to configure a pre-existing FAMOUS job.

## FAMOUS configuration

### MOSESI and MOSESII

Separate MOSESI and MOSESII.2 configurations are available. The base umui jobs can be used to build and run each of these. 

### UMUI

FAMOUS is configured via the umui as usual. The standard FAMOUS jobs have be rationalised to make their configuration as simple as possible. Details on this are below. The standard jobs are xmjne (MOSESI) or xmjnf (MOSESII) under user simon. All standard umui options are available, practically it is no different from running FAMOUS using a standard UM installation.

The "Submit" button DOES NOT WORK.
~~~
umsubmit_local -u pumauserid runid
~~~

on the local machine must be used instead.

There are three different modes of running, increasing in complexity.

 Simplest 
 : Run a copy of the base job without any alterations. This will work using the default start date and dumps and is ideal for testing the installation and timing studies.

 Normal
 : The standard umui jobs can be altered as usual changing items such STASH, start dumps, output directory location..., infact anything which doesn't require model recompilation.

 Full installation
 : If changes to the model or reconfiguration code are required, then a full installation is needed. This requires the Intel compiler, and a MPI installation. See below. 

### modsets

The difference between MOSESI and MOSESII modsets are considerable. In fact, MOSESII code
does not exist as part of the standard UM4.5 release and can only be configured as mods. Therefore it was decided that there should be different standard mods for each configuration. All of the various model mods for the two FAMOUS configurations are now held in 5 mods, these are:

 source_common.mod
 : FORTRAN mods which are common to both MOSESI and MOSESII

 source_common_c.mod
 : C mods which are common to both MOSESI and MOSESII

 source_MOSESI.mod
 : MOSESI exclusive mods

 source_MOSESII.mod
 : MOSESII exclusive mods

 port_end_f.mod
 : mod which allows IO on little endian machine, such as Linux. UM files are natively bigendian. It was decided to keep this separate to allow easy porting of a model configuration to a bigendian machine such as IBM Power.

Similarly there mods for the reconfiguration.

 recon_common.mod
 : FORTRAN mods which are common to both MOSESI and MOSESII

 recon_MOSESI.mod
 : MOSESI exclusive mods

 recon_MOSESII.mod
 : MOSESII exclusive mods


These mods are concatenations of the standard mods for each model. The tool $UMDIR/tools/make_mod.sh was used for this. Full details on the mods used are at the end of this documentation.

### handedits

The handedits where concatenated in a similar way to the modsets. There is a single handedit for each model configuration. They are `~simon/famous/handedit_MOSESI.sh` and `~simon/famous/handedit_MOSESII.sh` . The tool `make_handedit.sh` was used to create them. In those cases where the original handedit changed parameter values which could be set in the umui, these values where set directly in the umui and that part of the handedit discarded.


### Directories

An number of directories can be set by the user via environment variables. Depending on the directory type, this needs to be done either via the umui or via the user's `$HOME/.profile` .
Certain variables have to be set in the .profile as these are required by the UM system and
need to be set before the umui job is copied from puma for submission.

#### $HOME/.profile environment variables

***Required:***
 UMDIR
 : Directory of unpacked tarball. This should end with um_famous.
 
 DATA_DIR
 : Base model output directory. Note: `DATA_DIR` can also be set in the umui, and this will have precedence over the value in setvars.

See `example.profile` in `$UMDIR` for example settings.

***Optional:***
 TMPDIR
 : Temporary files, default `$DATA_DIR/tmp` . Do not set this to a shared filespace such as `/tmp` as this could cause issues if more than one person is running the UM on the machine.

MY_OUTPUT
 : Output .leave files produced as the model runs. Default `$DATA_DIR/umui_out`

MPICH_DIR
 : Set only if using local MPI version. See below. Default `$DATA_DIR/mpich3.2`

#### umui environment variables

 ARCHIVE_DIR
 : Directory where archived data and dumps are stored. Default `$DATA_DIR/um_archive/$RUNID`

FAMOUS_DATA
 : Directory of input data. Only needs to be changed to the input data directories are moved from under `$UMDIR`.


### Archiving

The model configurations uses the standard umui archiving system. Output data files are translated into PP before archiving, while the dumps are just copied. It can be turned off via the umui, if required.

## Intel FORTRAN, MPI and gcom

The model tarball comes complete with a pre-built MPICH3.2 system. The default installation is configured to use this. If the model needs recompilation, or
a different MPI system than MPICH3.2 is required to run the model (for example on some clusters), then the model needs to be recompiled on the local system.
Firstly Intel FORTRAN needs to be installed. In theory it is possible for this FAMOUS version to use other compilers, but currently only Intel FORTRAN is
supported. MPI has to be installed (if it hasn't been already). FAMOUS has been tested with MPICH3.2 but should work with other implementations. For MPICH3.2
follow the installation instructions at `https://www.mpich.org/` . It needs to be configured for Intel FORTRAN for both F77 and F90. Once it has
been installed, add the line
~~~
export MPI_DIR=/path/to/top/level/mpich
~~~
to your `.profile`, before the call to setvars, changing the path as required. If MPI is already installed, then add this line
to point to the local installation.

Alternatively, if you local system uses modules, ensure that the required MPI (and compiler if needed) modules are loaded when a session is started, normally be placing the module load command in `~/.profile`.
Then ensure that `$MPI_DIR` is not set and
~~~
export MPI_MODULES=Y
~~~
is.


Next gcom (the system the model uses for multi-processor communications) needs to be compiled using MPI. Type
~~~
cd $UMDIR/gcom3.8/gcom
make
~~~
 
The file `$UMDIR/gcom3.8/gcom/lib/libgcom_buffered_mpi.a` should now exist.

There is no need to recompile the reconfiguration unless there is a code change. The included executable independent of MPI.

The reconfiguration or model can now be compiled as usual. The standard compile system will use the MPI version defined in `MPICH_PATH` and the gcom version
in `$UMDIR/gcom3.8/gcom/lib`.

**IMPORTANT:** when compiling the model and reconfiguration, change the name of the output
executable to `$DATAW/$RUNID.exec` or `$DATAW/$RUNID.recon` otherwise there is a danger that the
standard executable under `UMDIR` will be overwritten.

## Configuration of a standard vn4.5 job to work with portable FAMOUS.

It is possible to take any vn4.5 umui configuration and make it work with portable FAMOUS. You need to copy the required mods and input data.

1. Copy the umui job.

2. Remove all script mods.

3. Remove any compile overrides.

4. Change the paths of the mods and input data to match the local paths.

All of the standard FAMOUS mods and ancillaries are included in the portable release, under `$UMDIR/mods/source` and `$UMDIR/data` respectively.

## Experimental: Cluster options for non-slurm systems.

There is an option to use a different job control system from slurm. This is currently in the experimental phase, and isn't guaranteed to work.

1. Copy `~simon/famous/bin/handedit_cluster.sh` 

2. In the FAMOUS umui job, go into ***Sub model Independent->Post Processing->Local post-processing scripts*** and set the path of the `handedit_cluster.sh` to your new file, and set "Include" to Y.

3. Edit the file, there are instructions in the script itself. You'll need to change the line 
~~~
export CLUSTER_OPTIONS=...
~~~
for your local job control system.

You will need to know three command line options for the local submission system:
1. How to specify the queue. This is optional. If it is not used, then the default queue is used. 
2. How to specify the output file path, and how to combine the standard out and error streams.
3. How to specify the name of the submitted job.

These options then take three environment variables as arguments (which MUST start with "\$"), `\$ACCOUNT` `\$OUTFILE` and `\$JOBNAME`.

**NOTE:** The environment variables are part of the FAMOUS system, and do not need to be set by the user.

You have to match the command line submit options to the each environment variable:

The line should start with the command used to submit jobs to the queue.

The option to `\$ACCOUNT` is optional and set in the umui. This can be used to specify the queue name or the charging account queue name. The appropriate command line flag has to be set.

The option to `\$OUTFILE` is required. It should follow the flag to specify the
output file path for the job. In addition, the option to combine
standard out and standard error should be included, this is normally
either "-j y" or "-j oe"

The option to `\$JOBNAME` is required. It is the name of the job when submitted to the queue.

For example:
~~~
export CLUSTER_OPTIONS="qsub -l proj -P \$ACCOUNT -o \$OUTFILE -j y -N \$JOBNAME"
~~~

 * "`qsub`" is the command to submit jobs to the job control system.

 * "`-l proj -P \$ACCOUNT`" specifies the queue to use, specified in the "Job submission" section of the umui, in this case, two command line arguments are required, "`-l proj`" is required by the local submission system.

 * "`-o`" specifies the output file path, and "-j y" combines standard out and error.

 * "`-N`" specifies the job name of the job.


## Changes from standard UM/FAMOUS

* Linux only.
* UM comes as a single pre-configured tarball.
* UM installation process no longer required.
* UM tools included in tarball.
* Scripts are hard coded, no script mods.
* All small executables are prebuilt as static executables.
* All mods grouped together into a small number of files.
* Compile system changed so that pre-built object files no longer required.
* All handedit file collated into a single file.
* umui jobs cleaned up.
* umui updated to set values directly which handedits overwrote. These handedits removed.
* umui system code updated.
* Dumps and ancils co-located.
* MPICH built and included with system for multi-processor models.
* Changed paths so that only minimal only two (UMDIR DATA_DIR) need changing.
* Ensured that system is flexible enough to allow UM experts to configure as they would a standard UM system.
* Archiving system fully integrated with model scripts.
* Fixed a ~~bug~~ feature in recon where environment variables cannot be used in user ancils paths.

## Mod sets.

The following mod sets where used for the standard jobs:

### Recon

Common mods:
~~~
abort.mod
dummy.mod
fix_ancil_name.mod
port_conv_f.mod
recon4837
recon_O.mod_xcggb
timerupd_new.mod
~~~

MOSESI mods:
~~~
ctile6
~~~

MOSESII mods:
~~~
arerf406_ctile
~~~

### Model

Common mods:
~~~
FHL_bugs.mod
LANDTOGLOBAL
PTOUV_LAND
PTOUV_SEA
UTOPIA_4p5_divUTw.mod
a2o_specifiedCO2.mod
abortfix.mod
alk_2.mod_4.7.mh
ask1f406
ask6f406
asm1f406
atmstep_flush.mod
boundsfix_famous.mod_xcpsa
boundsfix_hadocc.mod_xdbua
boundsfix_nonmpp.mod
boundsfix_vn4.5.mod
diagsw_inlansea.mod
dummy.mod
fixfill3a.mod
fixmeanctl.mf77
fixsolang.mod
fixspin3a.mod
fixstdia.mod
ftj1f405
gbc0f406
gdr2f406
gdr3f406
gnuml45.mod
gps0f406
gsm1f406
gsm2f406
gsm4f406.PUM
gsm5f406
gsm8f406
gsm9f406
h3dbqlim
inittime_info
linuxf_mpp.mod
long_output_names.mod
meadlengths.mod
medout44.mod
model_fix.mod
no_gcom_setopt.mf77
nomsrest
ofilter_mpp.mod
orbital_parameters-6.1.mod
orh0f406
osy1f405_change
params_in_namelist_famous.mod
polescon
port_conv_c.mod
port_conv_f.mod
port_end_c.mod
self_shade_safe.mod_4.5
stash80.mod
timerupd_new.mod
tjnowrit
tropin11.mod
tuning_2.mod_4.7.mf77
vflux_drift.mod_301015
~~~

MOSESI mods:
~~~
UVTOP_SEA
ccouple
ctile_09_new_param_ftlfix
inlansea_biogeo.mod
ozone_mod-3levcustom
schmidt_bounds.mod
snowonice_coupling.mod
stratcap.mod
t20db_mod45_adb1f406
~~~

MOSESII mods:
~~~
cap_sflintsea.mod
ccouple_moses2.2
co2_coupling_landfix_060912.mod
ice_drift_fix
icedrift_090912.mod
inlansea_biogeo_safer.mod
moses2.2_ctile_060912.mod
namelist_famous_land_060912.mod
namelist_famous_ocean_cc.mod
oco2_cap_060912.mod
ozone_mod-3levsane
rayleigh_fric.mod
snowonice_moses2.mod
~~~

These are included as part of the distribution under the `$UMDIR/mods` directory.
