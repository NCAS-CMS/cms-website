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

**Note:** Instructions cannot cover all possible suite setup combinations so you may need to adjust them accordingly. For example, tasks may be named slightly differently or inherit differently.

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

*  In panel *"postproc -> Post Processing - common settings -> Archer Archiving"* change **archive_root_path** to be a directory on the `/work` disk \\
For example; `/work/n02/n02/<username>/archive` where `<username>` is your ARCHER2 username.  \\
This will be a temporary area to stage your data before transfer to JASMIN.

* In panel *"postproc -> Post Processing - common settings -> JASMIN Transfer"*:
  * Set **transfer_type** to `Push`
  * Set **remote_host** to `gridftp1.jasmin.ac.uk` 
  * Set **gridftp** to `true`

**Note:**  See **u-be303/archer2** for a complete working postproc and pptransfer example suite.


