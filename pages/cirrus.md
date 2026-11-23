---
layout: page
title: Cirrus
subheadline: UK National Compute Resource
teaser: Cirrus is a state of the art HPC system hosted by <a href="https://www.epcc.ed.ac.uk">EPCC</a> at the <a href="https://www.ed.ac.uk">University of Edinburgh</a> and is one of the <a href="https://www.ukri.org">UKRI</a> National Compute Resources. 
permalink: /cirrus/
image:
    title: cirrus.jpg
---

## About Cirrus

Cirrus is an HPE Cray Ex4000 system with 640 compute nodes, each with dual AMD EPYC 9825 144-core processors, giving 184,320 cores in total. There are 576 standard memory nodes and 64 high memory nodes. Further details on the [Cirrus hardware](https://www.cirrus.ac.uk/about/hardware-software/) can be found on the [Cirrus website](https://www.cirrus.ac.uk).

## n02 on Cirrus

To request an account on Cirrus, follow [these instructions](https://epcced.github.io/safe-docs/safe-for-users/#your-user-account-on-the-service-machine). When asked to “Select correct project group” select: n02 - NCAS (National Centre for Atmospheric Science) from the drop down list.

To run UM rose/cylc workflows, users will also need an account on [PUMA2]({{ 'puma2' | relative_url }}). 

UM data and supporting software is stored on Cirrus under the `umshared` package account: `/epccfs/y07/shared/umshared`. 
If you have completed the [setup instructions](https://ncas-cms.github.io/um-training/getting-setup-selfstudy.html) this is equivalent to the `$UMDIR` environment variable.

See the [Unified Model pages]({{ 'unified-model' | relative_url }}) for more details of the UM infrastructure supported by CMS on Cirrus.

## Using Cirrus

Cirrus provide extensive [documentation](https://docs.cirrus.ac.uk/).  A summary of [differences from ARCHER2](https://docs.cirrus.ac.uk/archer2-migration-2026/cirrus-differences/) is also available.

Users can use [SAFE](https://safe.epcc.ed.ac.uk/) to query their disk usage and project resources. 

## UM transition from ARCHER2 to Cirrus

A list of standard workflows which CMS have ported to Cirrus along with instructions on how to port a non-standard configuration from ARCHER2 to Cirrus and general guidance will shortly be made available on the [porting pages](porting). 


