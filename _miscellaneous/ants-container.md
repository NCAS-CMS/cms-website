---
layout: page-fullwidth
title: ANTS
subheadline: Miscellaneous
teaser: The Met Office's ANcillary Tools and Suites is available in a Singularity container. It is available for download and is also installed on ARCHER2 and JASMIN.
---
## Introduction

ANTS aims to help you produce ancillary files. ANTS will help you when you want to do any of the following:

1. Produce ancillary files on a new model domain.
2. Produce a new set of ancillaries from new source data.
3. Derive a completely new set of ancillary fields for a new parametrisation scheme.

We have made ANTS available in a Singularity container. It is available for download and is also installed on ARCHER2 and JASMIN. It is not available on Monsoon2 as the OS is too old to use Singularity.

The latest ANTS version is v0.15. Documentation on ANTS is here: ​[https://code.metoffice.gov.uk/doc/ancil/ants/0.15/index.html](https://code.metoffice.gov.uk/doc/ancil/ants/0.15/index.html)

The container consists of the full ANTS anaconda environment.

​[IRIS](https://scitools-iris.readthedocs.io/en/stable/), [MULE](https://code.metoffice.gov.uk/doc/um/mule/2020.01.1/) and [​shumlib](https://code.metoffice.gov.uk/trac/utils/wiki/shumlib) are also installed in the container as dependencies.

The container uses ​[Singularity](https://sylabs.io/guides/3.7/user-guide/).

## Container details

### Locate or obtain container

Either:

* On ARCHER:

  `export ANTS_CONTAINER=/work/y07/shared/umshared/ANTS/latest/ants_latest.sif`

* On JASMIN:

  `export ANTS_CONTAINER=/home/users/siwilson/ANTS/latest/ants_latest.sif`

* Else obtain container from Singularity Cloud. Note: Singularity v3.5+ required:
~~~
  singularity pull library://simonwncas/default/ants:latest
  export ANTS_CONTAINER=/path/to/container/ants_latest.sif
~~~

## Usage details

The UM Ancillaries are required to run ANTS.

* On ARCHER these are in `$UMDIR/ancils`

* On JASMIN these are in `/gws/nopw/j04/rdf_migrate_vol1/umshared_backup/ancil`. \\
  You will need to apply to access the `rdf_migrate` GWS. 

To use the container:

`singularity shell [-B /gws/nopw/j04/rdf_migrate_vol1] $ANTS_CONTAINER`

Will start an interactive shell inside the container. The ANTS python environment and tools are then used as usual.` -B /gws/nopw/j04/rdf_migrate_vol1` is required on JASMIN to access the UM ancil directory.

`singularity exec [-B /gws/nopw/j04/rdf_migrate_vol1] $ANTS_CONTAINER ancil_general_regrid.py`

will run an ANTS application directly. This command can be aliased to replace the application call in a script. eg.

`alias ancil_general_regrid.py='singularity exec [-B /gws/nopw/j04/rdf_migrate_vol1] $ANTS_CONTAINER ancil_general_regrid.py'`

To start the ANTS enabled python directly

`singularity exec [-B /gws/nopw/j04/rdf_migrate_vol1] $ANTS_CONTAINER python`

The contrib tools are under `/opt/ants_contrib` in the container.


