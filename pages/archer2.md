---
layout: page
title: ARCHER2
subheadline: UK National Supercomputing Service
teaser: The ARCHER2 service is a world class advanced computing resource for UK researchers. ARCHER2 is provided by <a href="https://www.ukri.org">UKRI</a>, <a href="https://www.epcc.ed.ac.uk">EPCC</a>, <a href="https://www.cray.com"> HPE Cray</a> and the <a href="https://www.ed.ac.uk">University of Edinburgh</a>.
permalink: /archer2/
image:
    title: archer2-1200x716.jpg
---

## About ARCHER2

ARCHER2 is an HPE Cray EX supercomputing system with an estimated peak performance of 28 PFLOP/s. The machine has 5,860 compute nodes, each with dual AMD EPYC 7742 64-core CPUs at 2.25GHz, giving 750,080 cores in total. Further details on the [ARCHER2 hardware](https://www.archer2.ac.uk/about/hardware.html) can be found on the [ARCHER2 website](https://www.archer2.ac.uk).

## n02 on ARCHER2

To request an ARCHER2 account, follow [these instructions](https://docs.archer2.ac.uk/quick-start/quickstart-users/#request-an-account-on-archer). When asked to “Select correct project group” select: n02 - NCAS (National Centre for Atmospheric Science) from the drop down list.

To run UM rose/cylc workflows, users will also need an account on [PUMA2]({{ 'puma2' | relative_url }}). 

UM data and supporting software is stored on ARCHER2 under the `umshared` package account: `/work/y07/shared/umshared`. 
If you have completed the [setup instructions](https://ncas-cms.github.io/um-training/getting-setup-selfstudy.html) this is equivalent to the `$UMDIR` environment variable.

See the [Unified Model pages]({{ 'unified-model' | relative_url }}) for more details of the UM infrastructure supported by CMS on ARCHER2. 

## Using ARCHER2

ARCHER2 provide extensive [documentation](https://docs.archer2.ac.uk/) and [training materials](https://www.archer2.ac.uk/training/). 

Users can use [SAFE](https://safe.epcc.ed.ac.uk/) to query their disk usage and project resources. 

For CMS advice on ARCHER2 storage and managing disk space see: [ARCHER2 storage](storage). 
