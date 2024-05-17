---
layout: page-fullwidth
title: UM Postproc App
subheadline: Information on NCAS supported postproc versions on ARCHER2
permalink: '/unified-model/postproc/'
breadcrumb: true
---
{% include alert info="This page is currently under development." %}

There are currently 3 officially supported versions of the UM Post-processing app.  This page details each one
and under which circumstances you should use each.

## Postproc 2.3
There are 2 postproc branches at postproc_2.3.  The first is the updated old ARCHER branch which a lot of suites still use,
the second is the rewrite for ARCHER2 which includes the ability to migrate data to JASMIN Elastic Tape. 

### postproc_2.3_pptransfer_gridftp_nopw

Includes PPTransfer code using Gridftp with certificates for automatic transfer of data from ARCHER2 to JASMIN.
It **DOES NOT** include the ability to migrate data to JASMIN Elastic Tape.

Use the following suite settings in *fcm_make_pp -> Configuration*

**Atmosphere only suites:**
~~~
config_base=fcm:moci.xm-tr
config_rev=@postproc_2.3
pp_rev=postproc_2.3
pp_sources=fcm:moci.xm-br/dev/rosalynhatcher/postproc_2.3_pptransfer_gridftp_nopw
~~~

**Coupled suites:**
~~~
config_base=fcm:moci.xm-br/dev/annetteosprey/postproc_2.3_archer2
config_rev=
pp_rev=postproc_2.3
pp_sources=fcm:moci.xm-br/dev/annetteosprey/postproc_2.3_archer2 fcm:moci.xm-br/dev/rosalynhatcher/postproc_2.3_pptransfer_gridftp_nopw
~~~

### postproc_2.3_archer2_jasmin_rewrite

This branch includes ability to transfer data to JASMIN using gridftp with certificates as well as the option to migrate
the transferred data to JASMIN Elastic Tape.

~~~
config_base=fcm:moci.xm-br/dev/rosalynhatcher/postproc_2.3_archer2_jasmin_rewrite
config_rev=
pp_rev=postproc_2.3
pp_sources=fcm:moci.xm-br/dev/rosalynhatcher/postproc_2.3_archer2_jasmin_rewrite
~~~

## Postproc 2.4
