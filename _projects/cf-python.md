---
title: CF Python
type: core
teaser: The Python cf package is an Earth Science data analysis library that is built on a complete implementation of the [CF data model](https://ncas-cms.github.io/cf-python/cf_data_model.html#cf-data-model).
status: active
---

CF is a netCDF convention which is in wide and growing use for the storage of model-generated and observational data relating to the atmosphere, ocean and Earth system.

The [cf-python](http://cfpython.bitbucket.org/) package is an implementation of the CF data model, and as such it is an API allows for the full scope of data and metadata interactions described by the CF conventions.

### Current work

* The first stable release is out (available from [PyPI](https://pypi.python.org/pypi/cf-python))
* Documentation overhaul

### Upcoming features

* Regridding using the [ESMF](https://www.earthsystemcog.org/projects/esmpy/) library. This powerful package will allow bi-linear and fully conservative regridding on a sphere in latitude-longitude and projected coordinate systems, as well as arbitrary cartesian regridding. 
