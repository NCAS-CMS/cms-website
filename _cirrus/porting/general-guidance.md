---
layout: page-fullwidth
title: General Guidance
subheadline: Porting a UM suite to Cirrus
permalink: '/cirrus/porting/general-guidance/'
breadcrumb: true
---

## Serial Nodes

There are no serial nodes on Cirrus.  Jobs that used to run on the ARCHER2 serial nodes should be configured to run on a compute node non-exclusively.

## Globus

Advise to run pptransfer tasks on a login node (cylc use platform = cirrus-bg) to avoid being changed for data transfer and needing to have .globus file in /epccfs??????

## Efficient use of Compute Nodes

Add information here regarding importance of making sure nodes are being fully used to avoid unnecessary charging.  Remember if your job is using a compute node exclusively, then you will be charged for all cores irrespective of whether you are using all 288 or not.

## PUMA2

 * Make sure connecting to PUMA2 using the recommended method, this is also required for using the Cylc 8 Web UI
 * On Cirrus make sure you have sourced the rose-env-puma2 Rose/Cylc environment file.
 * Add Cirrus key to your ssh-agent on PUMA2
