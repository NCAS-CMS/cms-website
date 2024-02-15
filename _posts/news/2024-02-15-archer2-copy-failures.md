---
layout: page
subheadline:  "Announcement"
title:  "ARCHER2 File copy failures"
teaser: "We have been alerted to a problem copying files on the ARCHER2 /work/n02/n02 file system. The problem is associated with the python shutil file copy functions and results in incomplete file copying."
categories:
    - news
tags:
    - news
    - archer2
    - um
author: ros
#header: no
---

The error will potentially affect all Rose/Cylc suites that use the postproc app, which stages data on ARCHER2 prior to transferring it to JASMIN.

As a matter of urgency:

1. All suites that use postproc should be paused now.
2. Users need to check on ARCHER2 that post-processed data is complete and not corrupted.
3. Users need to check on JASMIN group workspace and tape that post-processed data is complete and not corrupted.

CMS will deploy a fix to postproc shortly.

If data corruption has occurred, UM suites will need to be re-run.

{% comment %} Leave below here {% endcomment %}
## All News Items
{: .t60 }

{% include list-posts tag='news' %}
