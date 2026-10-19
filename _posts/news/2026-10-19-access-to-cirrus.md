---
layout: page
subheadline:  "HPC Announcement"
title:  "Access to Cirrus"
teaser: "If your project has been awarded time on Cirrus (the PI should have received an award letter from UKRI), you can apply for a Cirrus account through the [SAFE system](https://safe.epcc.ed.ac.uk/)."
categories:
    - news
tags:
    - news
    - cirrus
author: ros
#header: no
---

## Access to Cirrus

If your project has been awarded time on Cirrus (the PI should have received an award letter from UKRI), you can apply for a Cirrus account through the [SAFE system](https://safe.epcc.ed.ac.uk/).

Go to Login accounts → Request login account, select the "n02" project and choose "Cirrus" as the machine.

Note: Your Cirrus username must match your ARCHER2 username.

Project budget codes are unchanged from ARCHER2 and have been populated with the awarded allocations, where appropriate.

The Cirrus work filesystem is located at `/epccfs/n02`. To facilitate the transfer of essential data, this filesystem is also mounted on ARCHER2 at `/nscds/n02`.

**Please transfer only essential files to Cirrus.** The n02 disk quota is the same as on ARCHER2. Please do not simply transfer all files across otherwise we will run out of space quite quickly. Please take this opportunity to remove unwanted files. Only active files needed to run your simulations should be stored on Cirrus; output data should be moved to other storage, e.g. JASMIN.

Guidance on transferring data to Cirrus, including using rclone, is available in the [ARCHER2 documentation](https://docs.archer2.ac.uk/user-guide/data/#local-file-transfer).


## IMPORTANT: Unified Model Users

You can apply for an account on Cirrus (if your project has been awarded time) and transfer over essential data, but you will not yet be able to run UM workflows. Please continue to use your ARCHER2 budget until the end of the ARCHER2 service. NCAS-CMS are working hard to set up the UM, associated infrastructure and to provide documentation on how to upgrade your workflows to run on Cirrus. We will announce when the UM is available for use.

Not all UM versions currently available on ARCHER2 will be installed on Cirrus. Initially we will focus on versions 13.5-13.9, 14.x. A few other older key UM versions will also be installed where there is an identified need; e.g. CMIP6. Other versions will be considered on a case-by-case basis.

With the move to Cirrus, Cylc 7 will be officially retired, and all workflows will need to use Cylc 8.

PUMA2 will continue to act as the Cylc workflow server and will work with Cirrus in the same way as it does with ARCHER2. We are working with EPCC to reconfigure PUMA2, and users will need to undertake a small amount of transition work. We will make a further announcement when the timescales and required actions are confirmed.

If you have any questions please raise a ticket on the NCAS-CMS helpdesk: https://cms-helpdesk.ncas.ac.uk/

{% comment %} Leave below here {% endcomment %}
## All News Items
{: .t60 }

{% include list-posts tag='news' %}
