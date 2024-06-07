---
layout: page-fullwidth
title: UM Post-processing App
subheadline: Information on NCAS supported postproc versions on ARCHER2
permalink: '/unified-model/postproc/'
breadcrumb: true
---
{% include alert info="This page is currently under development." %}

This document details how to upgrade the version of postproc in your suite to include tasks to:

1. Transfer data to JASMIN using Gridftp
2. Migrate data to JASMIN Elastic Tape
  
## Upgrading Postproc to use the ARCHER2/JASMIN branch

#### 1. Determine which version of Postproc your suite is currently using

In panel *'fcm_make_pp -> Configuration'*, if **config_rev** and/or **pp_rev** is

* **postproc_2.3**
  * Follow instructions below substituting `X.Y` with `2.3` and `ppXY_t588` with `pp23_t588`

    
* **postproc_2.4**
  * Follow instructions below substituting `X.Y` with `2.4` and `ppXY_t588` with `pp24_t588`
 
#### 2. Set branches for fcm_make_pp app

* In panel *'fcm_make_pp -> Configuration'* set

  ~~~
  config_base=fcm:moci.xm-br/dev/rosalynhatcher/postproc_X.Y_archer2_jasmin_rewrite
  config_rev=
  pp_rev=postproc_X.Y
  pp_sources=fcm:moci.xm-br/dev/rosalynhatcher/postproc_X.Y_archer2_jasmin_rewrite
  ~~~

  Where `X.Y` is either `2.3` or `2.4` depending on which version of postproc your suite is using.

* Save and Exit the Rose edit GUI

#### 3. Upgrade postproc app to ppXY_t588

* Run rose app-upgrade

  ~~~
  cd app/postproc
  rose app-upgrade -M /home/n02/n02/ros/meta/postproc_X.Y_archer2_jasmin_rewrite/rose-meta -a ppXY_t588
  ~~~

  Where `X.Y` is either `2.3` or `2.4` and `ppXY_t588` is either `pp2.3_t588` or `pp2.4_t588` as appropriate

  Type `y` when prompted to "Accept y/n"

* Edit `app/postproc/rose-app.conf` to set

  ~~~
  meta =  /home/n02/n02/ros/meta/postproc_X.Y_archer2_jasmin_rewrite/rose-meta/archive_and_meaning/postproc/ppXY_t588
  ~~~

* Launch new Rose Edit window: `rose edit`

* Navigate to *'postproc -> Post Processing - common settings -> ARCHER2-JASMIN'*. You should see one panel labelled "Data Transfer".  To load the JASMIN ET panel go to menu option **'View'** and select **'View latent pages'**. A new grayed out panel *'Elastic Tape'* should appear.

* R click on the greyed out "Elastic Tape" and select "add namelist:jasmin_arch".

* Click on the red `+` sign against each variable in the panel (`default_workspace`, etc) and select **"Add to configuration"**

* Save and Close the Rose Edit GUI.

#### 4. Add in the JDMA configuration file and suite metadata:

* Copy standard config files
  
  ~~~
  cp ~um1/jdma/jdma.rc ~/roses/<suiteid>
  cp ~um1/jdma/metadata/ncas_extras ~/roses/meta
  ~~~

* In `suite.rc` file add the following line to the bottom:

  {% raw %}
  ~~~
  {% include 'jdma.rc'}
  ~~~
  {% endraw %}

* In `meta/rose-meta.conf` add the following line to the top of the file:

  ~~~
  import=meta/ncas_extras
  ~~~

* Open Rose Edit GUI and under *'suite conf -> JASMIN Elastic Tape'* click on the red `+` sign next to "Migrate data to JASMIN Elastic Tape" select **"Add to configuration"**

* Save

#### 5. Automatically delete data from ARCHER2 after successful transfer to JASMIN

If you are transferring data to JASMIN please add the following to the Housekeeping app to activate deletion of data from ARCHER2 following successful transfer to JASMIN.\

* In *'app/housekeeping/rose-app.conf'* add:

  ~~~
  prune{share/cycle}=-P6M
  ~~~


#### 6. Configure PPTransfer and JDMA tasks

Now follow the instructions on how to configure [PPTransfer to JASMIN](pptransfer) and optionally [Data migration to Elastic Tape](jdma).
