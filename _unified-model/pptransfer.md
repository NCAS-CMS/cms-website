---
layout: page-fullwidth
title: Configuring PPTransfer
subheadline: Data Transfer from ARCHER2 to JASMIN
permalink: '/unified-model/pptransfer/'
breadcrumb: true
---
The now-recommended method for transferring data between ARCHER2 and JASMIN is using GridFTP using certificate authentication.  This allows data transfers to run on the ARCHER2 serial nodes using certificate-based authentication rather than SSH.  Certificates are valid for up to a month from initiation and can be easily extended/regenerated for longer running simulations.

These instructions show how to setup your GridFTP certificate and modify a suite to run the `pptransfer` task on the ARCHER2 serial nodes to push the data across to JASMIN from ARCHER2 `/work` disk. 

**Note:** In order to use GridFTP to JASMIN you must have access to the **hpxfer (High Performance Data Transfer Service)**. Access can be requested via the [JASMIN Accounts Portal](https://accounts.jasmin.ac.uk/).

## Obtaining a JASMIN short-lived credential

* Login to ARCHER2.

* Change directory to your ARCHER2 work directory - `/work/n02/n02/USERNAME`.  

* [First Time Only] "Bootstrap trust" to setup your local certificate store with those needed to interact with the JASMIN server.
~~~
  $ $UMDIR/bin/onlineca-get-trustroots-wget.sh -U https://slcs.jasmin.ac.uk/trustroots/ -b
  Bootstrapping Short-Lived Credential Service root of trust.
  Trust roots have been installed in /home/n02/n02/USERNAME/.globus/certificates.
~~~

* Obtain a short-term credential (this must be called `cred.jasmin`) using your JASMIN accounts portal username USERNAME.
~~~
$ $UMDIR/bin/onlineca-get-cert-wget.sh -U https://slcs.jasmin.ac.uk/certificate/ -l USERNAME -o ./cred.jasmin
~~~
When prompted for a passphrase, this is the password associated with your **JASMIN** account portal account (**NOT your SSH passphrase**)

* Change the permissions on the newly-created `cred.jasmin` file so that it is only readable by you.

  `$ chmod 600 cred.jasmin`

This credential is valid, by default, for 30days.  You can see the validity period by inspecting the certificate using the following command:
~~~
$ openssl x509 -in cred.jasmin -noout -startdate -enddate
notBefore=Mar 11 17:32:59 2022 GMT
notAfter=Apr 10 17:32:59 2022 GMT
~~~

This means you can use this certificate for the following 30days, after which you will need to repeat this step to obtain a new one.

A fuller explanation of the process is given in the document [Data Transfer Tools: GridFTP (certificate-based authentication)](https://help.jasmin.ac.uk/article/3808-data-transfer-tools-gridftp-cert-based-auth)

## Suite Settings

These settings assume you are using the ARCHER2/JASMIN version of postproc as detailed on the [Post-Processing page](/unified-model/postproc) and wish to automatically delete data from ARCHER2 after successful transfer to JASMIN.

*  In panel *"postproc -> Post Processing - common settings -> ARCHER2-JASMIN Archiving"* set **archive_root_path** to be `$ROSE_DATAC`.  This evaluates to `cylc-run/<suiteid>/share/cycle`.  

* In panel *"postproc -> Post Processing - common settings -> ARCHER2-JASMIN Archiving -> Data Transfer"*:
  * Set **transfer_dir** to be a directory on your Jasmin group workspace (e.g. `/gws/nopw/j04/ncas_cms/aosprey/archive`) or on the [JASMIN Transfer Cache](https://help.jasmin.ac.uk/docs/short-term-project-storage/xfc/) (e.g. `/work/xfc/vol5/user_cache/rshatcher/archive`)
  * Set **transfer_type** to `Push`
  * Set **remote_host** to `gridftp1.jasmin.ac.uk` 
  * Set **gridftp** to `true`

**Note:**  See **u-bc613/archer2** for a complete working postproc and pptransfer example suite.


