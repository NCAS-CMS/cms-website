---
layout: page-fullwidth
title: Configuring PPTransfer using Globus
subheadline: Data Transfer from ARCHER2 to JASMIN
permalink: '/unified-model/pptransfer-globus/'
breadcrumb: true
---
JASMIN will be retiring the current gridftp server (gridftp1.jasmin.ac.uk) in December 2024.
This means that everyone will need to use Globus (https://docs.globus.org/) for data transfers between ARCHER2 and JASMIN.

There is some initial setup to do, including authenticating to the ARCHER2 and JASMIN Globus endpoints.  As with gridftp
authentication certificates are only valid for 30 days.  This means you will need to manually re-authenticate every 30 days
to allow transfers to continue.

The following instructions show how to setup Globus, authenticate to ARCHER2 and JASMIN endpoints, and modify a suite to 
run the `pptransfer` task on the ARCHER2 serial nodes to push the data across to 
JASMIN from ARCHER2 `/work` disk. 

Further information on Globus, including how to setup up one-off data transfers can be found here: https://docs.globus.org/

## Setting up Globus for ARCHER2

https://docs.archer2.ac.uk/data-tools/globus/#setting-up-archer2-filesystems

Stop when you reach the section "Setting up the other end of the transfer".

## Setting up Globus for JASMIN

Complete steps 1-9 here:
https://help.jasmin.ac.uk/docs/data-transfer/globus-transfers-with-jasmin/

# Setting up Globus CLI on ARCHER2

https://docs.globus.org/cli/

**Note:** Have asked ARCHER2 if a central install of Globus CLI can be installed to save everyone having to do this.
Alternatively, we could put an installation under `umshared` I suppose.




