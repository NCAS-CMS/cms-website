---
layout: page-fullwidth
subheadline: PUMA2
title: PUMA2
permalink: /puma2/
---

The PUMA2 service was setup by NCAS-CMS to provide the UK research community with centralised access to the UM on ARCHER2 and other national HPCs. 
It hosts mirrors of the Met Office Science Repositories and provides access to Rose & Cylc enabling submission of model simulations to ARCHER2 and other machines. 

PUMA2 is hosted at ARCHER2 and jointly managed by CMS and EPCC. PUMA2 access is managed through the SAFE system. 

## Applying for an account

You need to request a PUMA2 account through SAFE. 

If you don't already have an ARCHER2 account, follow [these instructions first](https://docs.archer2.ac.uk/quick-start/quickstart-users/#request-an-account-on-archer). 
When asked to *“Select correct project group”* select: **n02 - NCAS (National Centre for Atmospheric Science)** from the drop down list.

To request a PUMA2 account. 
* Login to [SAFE](https://safe.epcc.ed.ac.uk/)
* From the "Login accounts" menu, select your username
* Scroll down near the bottom, and select "Add Machine"
* At the bottom of the next page, under "Machine to join", select "puma2", and click "Join"

You will be sent an email when your PUMA2 account is ready for use. 

## Accessing PUMA2

PUMA2 is accessed from the ARCHER2 login nodes, and you will use the same username and password. 

* [Login to ARCHER2](https://docs.archer2.ac.uk/quick-start/quickstart-users/#login-to-archer2) as usual.

**Important:** We recommend users ***do not forward their ssh-agent*** from their local system, 
as this can cause problems with Rose/cylc job submission.

* Once you are on the ARCHER2 login nodes, type ```ssh -Y puma2```. Enter your ARCHER2 password when prompted.
  
* You should now be logged into PUMA2.

## Running the UM on ARCHER2

Follow the [setup instructions](https://ncas-cms.github.io/um-training/getting-setup-selfstudy.html) in our online training to configure your environment to run UM suites on ARCHER2. 

For more information on running UM jobs see our documentation: 
* [Unified Model]({{ '/unified-model/'| relative_url }}) 
* [Rose/cylc]({{ '/rose-cylc/'| relative_url }}) 
* [UMUI](umui)
