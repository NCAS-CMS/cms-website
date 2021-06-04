---
layout: page
subheadline:  "ARCHER2"
title:  "What storage is available on ARCHER2?"
teaser: "There are currently two data storage areas on ARCHER2 accessible by NCAS users."
group: archer2
author: ros
---
* HOME file system:

  `/home/n02/n02/<userid>`

  The home file system is fully backed up by ARCHER2.  This area is small and so an NCAS user allocation is therefore relatively small.  The compute nodes cannot see the HOME file system, all files required by running jobs must be located on the WORK file system. 

* WORK file system: 

  `/work/n02/n02/<userid>`

  The work file sytem is NOT backed up and is the only disk space accessible by ARCHER2 batch jobs.  NCAS has a large allocation and so an NCAS user allocation can be relatively large. 

For more information on the ARCHER2 file systems and how to access the HOME filesystem backup see: [ARCHER2 Storage](https://docs.archer2.ac.uk/user-guide/data/#archer2-storage).


{% comment %} Leave below here {% endcomment %}
## All FAQ Items
{: .t60 }

{% include list-collection collection='faq' %}
