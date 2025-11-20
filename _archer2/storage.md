---
layout: page-fullwidth
title: ARCHER2 storage
teaser: Information on the ARCHER2 storage systems and advice for managing user disk space.
permalink: '/archer2/storage/'
breadcrumb: true
---

## ARCHER2 storage 

Users have access to 3 file systems on ARCHER2:
- Home file systems (/home)
- Work file systems (/work)
- Solid state (NVMe) file system (/scratch)

Only the work and NVMe file systems can be seen from the batch nodes. 
The NVMe file system should give good and consistent performance for parallel I/O 
but it is subject to a strict 28 day deletion policy.

Full details on each of the file systems, including how to check quotas, can be found in the 
[ARCHER2 storage documentation](https://docs.archer2.ac.uk/user-guide/data/#archer2-storage)

## Managing disk space 

The n02 work file system is a finite resource, and shared amongst many users. 

Recently the n02 space has been operating very close to the project quota. EPCC have found that when the file system gets too near the quota it can cause severe issues, such as [job timeouts and data corruption](https://docs.archer2.ac.uk/known-issues/#when-close-to-storage-quota-jobs-may-slow-down-or-produce-corrupted-files-added-2024-02-27).

***It is crucial that all users carefully manage and minimise their data volume.***

Some advice for managing data from Rose/Cylc workflows: 

* **Check your disk usage**
  Archer2 provide instructions for [checking your quota and current disk usage](https://docs.archer2.ac.uk/user-guide/data/#quotas-on-the-work-file-systems).
  You can also use the `du` command to check the sizes of individual directories.

* **Tidy up old `cylc-run` directories.**
  * Clear out data from old experiments that you no longer need. 
  * Be sure to follow the symlinks to delete directories under `/work/n02/n02/$USER/cylc-run`
  * Check data in the `$DATADIR/archive` directory. 
  * Even if workflows have been set up with archiving, there can be copies of data left behind in `cylc-run`. Check the `share/cycle/`, `share/data` and `work/` sub-directories.


* **Check if you have any "shared" data.**
  Data owned by you under `/work/n02/shared/` and `/work/n02/n02/shared` still counts towards your quota. To check if you have any directories in these locations:
``` 
ls -l /work/n02/shared | grep $USER
ls -l /work/n02/n02/shared | grep $USER
```

* **Check the STASH output for your simulations** It is easy to keep adding in new diagnostics but take some time to check whether there fields or packages that could be switched off. Some suites are set up to output the same variable to multiple streams.

* **Use the NVMe scratch disk if possible.**
  It should be safe to use NVMe for simulations where data is being automatically archived,
  as long as you monitor your workflow.
  * For Cylc 8 workflows, use the `archer2-nvme` and `archer2-nvme-bg` platforms.
  * For Cylc 7 workflows, add the following lines to the top of your `rose-suite.conf` file:
```
root-dir{share}=ln*=/mnt/lustre/a2fs-nvme/work/n02/n02/$USER
root-dir{work}=ln*=/mnt/lustre/a2fs-nvme/work/n02/n02/$USER
```

* **Archive simulation output to an external system.**
  Archer2 is not intended for long-term data storage.
  See the documentation for how to:
  * [transfer data to JASMIN using Globus]({{ 'unified-model/pptransfer-globus' | relative_url }}) and 
  * [migrate data to JASMIN elastic tape]({{ 'unified-model/jdma' | relative_url }})
