---
layout: page-fullwidth
title: Configuring PPTransfer using Globus
subheadline: Data Transfer from ARCHER2 to JASMIN
permalink: '/unified-model/pptransfer-globus/'
breadcrumb: true
---
JASMIN will be retiring the current gridftp server (gridftp1.jasmin.ac.uk) in December 2024.
This means that everyone will need to use [Globus](https://docs.globus.org/) for data transfers between ARCHER2 and JASMIN.

There is some initial setup to do, including authenticating to the ARCHER2 and JASMIN Globus endpoints (collections).  As with gridftp
authentication certificates are only valid for 30 days.  This means you will need to manually re-authenticate every 30 days
to allow transfers to continue.

The following instructions show how to register for and setup Globus, as well as authenticate to the ARCHER2 and JASMIN endpoints.

Further information on Globus, including how to setup up one-off data transfers can be found here: https://docs.globus.org/

### 1. Setting up Globus for ARCHER2

* [Setting up ARCHER2 Filesystems](https://docs.archer2.ac.uk/data-tools/globus/#setting-up-archer2-filesystems)

  Stop when you reach the section "Setting up the other end of the transfer".

### 2. Setting up Globus for JASMIN

* Complete steps 1-9 here:  
  [Setting up JASMIN Filesystems](https://help.jasmin.ac.uk/docs/data-transfer/globus-transfers-with-jasmin/)

### 3. Authenticate to Globus using CLI

* Load Globus module

  ```
  ARCHER2> module load globus-cli
  ```
  
* Login to Globus

  ```
  ARCHER2> globus login
  ```

  Copy and paste the resulting url into your web browser and follow the instructions.

  You should get similar to the following on successfully completion:

  ```
  ARCHER2> globus login
  Please authenticate with Globus here:
  ------------------------------------
  https://auth.globus.org/v2/oauth2/authorize?client_id=6bc10e81-1f06-4b9d-8558-38f8df88617b&
  redirect_uri=https%3A%2F%2Fauth.globus.org%2Fv2%2Fweb%2Fauth-code&scope=openid+profile+
  email+urn%3Aglobus%3Aauth%3Ascope%3Aauth.globus.org%3Aview_identity_set+urn%3Aglobus%3Aauth%
  3Ascope%3Atransfer.api.globus.org%3Aall+urn%3Aglobus%3Aauth%3Ascope%3Agroups.api.globus.org%3
  Aall+urn%3Aglobus%3Aauth%3Ascope%3Asearch.api.globus.org%3Aall+https%3A%2F%2Fauth.globus.org%2F
  scopes%2F524230d7-ea86-4a52-8312-86065a9e0417%2Ftimer%5Bhttps%3A%2F%2Fauth.globus.org%2Fscopes%2F
  actions.globus.org%2Ftransfer%2Ftransfer%5Burn%3Aglobus%3Aauth%3Ascope%3Atransfer.api.globus.org%3A
  all%5D%5D+https%3A%2F%2Fauth.globus.org%2Fscopes%2Feec9b274-0c81-4334-bdc2-54e90e689b9a%2F
  manage_flows+https%3A%2F%2Fauth.globus.org%2Fscopes%2Feec9b274-0c81-4334-bdc2-54e90e689b9a%2F
  view_flows+https%3A%2F%2Fauth.globus.org%2Fscopes%2Feec9b274-0c81-4334-bdc2-54e90e689b9a%2F
  run+https%3A%2F%2Fauth.globus.org%2Fscopes%2Feec9b274-0c81-4334-bdc2-54e90e689b9a%2F
  run_status+https%3A%2F%2Fauth.globus.org%2Fscopes%2Feec9b274-0c81-4334-bdc2-54e90e689b9a%2F
  run_manage&state=_default&response_type=code&access_type=offline&prompt=login
  ------------------------------------
  Enter the resulting Authorization Code here: eDVZym2YOuz7zONxF5UB3g0IhiStk4
  You have successfully logged in to the Globus CLI!
  You can check your primary identity with
    globus whoami
  For information on which of your identities are in session use
    globus session show
  Logout of the Globus CLI with
    globus logout
  ```

* Check your identity:
  ```
  ARCHER2> globus whoami
  For information on which identities are in session see
    globus session show
  rosalyn.hatcher@ncas.ac.uk@accounts.google.com
  ```

* Check that your have both ARCHER2 and JASMIN linked identities
  ```
  ARCHER2> globus whoami --linked-identities
  For information on which identities are in session see
    globus session show
  rosalyn.hatcher@ncas.ac.uk@accounts.google.com
  ros@safe.archer2.ac.uk
  rshatcher@accounts.jasmin.ac.uk
  ```

### 5. Run CLI-based check

* Check everything is setup correctly by running a quick manual CLI-based check:

  `ARCHER2> globus ls 3e90d018-0d05-461a-bbaf-aab605283d21:/~/`

  Follow the instructions.

* Once consent has been given run the command again and it should then list your `$HOME` directory.

  ```
  ARCHER2> globus ls 3e90d018-0d05-461a-bbaf-aab605283d21:/~/
  23cab/
  archer_home/
  bin/
  cylc-run/
  cylc-suites/
  hpc-portal-backup/
  output/
  scripts/
  software/
  temp/
  ```

* Repeat for JASMIN endpoint
   
  `ARCHER2> globus ls a2f53b7f-1b4e-4dce-9b7c-349ae760fee0:/~/`

  Follow the instructions.

* Rerun `globus ls a2f53b7f-1b4e-4dce-9b7c-349ae760fee0:/~/` and it should list your JASMIN home directory.


### 6. Link .globus directory

* Setup a symlink to your `.globus` directory
  
  ```
  ARCHER2> cd /work/n02/n02/<archer2_username>
  ARCHER2> ln -s ~/.globus .globus
  ```

You should now be setup to use Globus through a UM workflow.




