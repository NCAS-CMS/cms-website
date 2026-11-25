---
layout: page-fullwidth
title: General Guidance
subheadline: Porting a UM suite to Cirrus
permalink: '/cirrus/porting/general-guidance/'
breadcrumb: true
---

{% include alert warning='Under Development' %}

## General PUMA2/Cirrus setup info

### Setting up connection to PUMA2

It is no longer possible to use a passphraseless key to connect from Cirrus login nodes to PUMA2.  The recommended method to login to PUMA2 is by using port-forwarding;  this is setup is also required in order to use the Cylc 8 web UI. Please see [Connection to PUMA2 via Cirrus](https://cms-helpdesk.ncas.ac.uk/t/connecting-to-puma2-via-cirrus/2232) on the CMS Helpdesk. Please do not use ssh-agent forwarding as this can cause problem with Cylc. 

### Add Cirrus ssh-key to your ssh-agent on PUMA2

```
puma2$ ssh-add ~/.ssh/<your-cirrus-key>
```

### Setting up environment on Cirrus

Make sure you have the following line in your `~/.bash_profile` on Cirrus:

```
# Setup environment for running the UM under Rose
. /work/y07/shared/umshared/bin/rose-um-env-puma2
```

## Serial Nodes

There are no serial nodes on Cirrus.  Jobs that used to run on the ARCHER2 serial nodes should be configured to run on a compute node non-exclusively.

## Globus 

**TODO** Advise to run pptransfer tasks on a login node (cylc use platform = cirrus-bg) to avoid being changed for data transfer and needing to have .globus file in /epccfs??????

## Efficient use of Compute Nodes

**TODO:** Add information here regarding importance of making sure nodes are being fully used to avoid unnecessary charging.  Remember if your job is using a compute node exclusively, then you will be charged for all cores irrespective of whether you are using all 288 or not.



