---
layout: page-fullwidth
title: UM Post-processing App
subheadline: Information on NCAS supported postproc versions on ARCHER2
permalink: '/unified-model/postproc/'
breadcrumb: true
---
{% include alert info="This page is currently under development." %}

There are currently 3 officially supported versions of the UM Post-processing app.  This page details each one, under which circumstances you should use each and how to upgrade your suite to use it.

## Determine which version of Postproc your suite is currently using

In panel *'fcm_make_pp -> Configuration'* 

If **config_rev** and/or **pp_rev** is
* postproc_2.3
  
  * Follow instructions: Upgrade postproc for Data Transfer/Elastic Tape for Postproc 2.3
    
* postproc_2.4

  * Follow instructions to upgrade postproc for Data Transfer/Elastic Tape for Postproc 2.4
  
## Postproc 2.3

This branch includes ability to transfer data to JASMIN using gridftp with certificates as well as the option to migrate
the transferred data to JASMIN Elastic Tape.

~~~
config_base=fcm:moci.xm-br/dev/rosalynhatcher/postproc_2.3_archer2_jasmin_rewrite
config_rev=
pp_rev=postproc_2.3
pp_sources=fcm:moci.xm-br/dev/rosalynhatcher/postproc_2.3_archer2_jasmin_rewrite
~~~

## Postproc 2.4
