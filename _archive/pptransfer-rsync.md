---
layout: page-fullwidth
title: Configuring PPTransfer
subheadline: Data Transfer from ARCHER2 to JASMIN
permalink: '/archer2/pptransfer/'
breadcrumb: true
---
The `pptransfer` task used to run on the ARCHER Data Transfer Node (dtn02) which we no longer have access to. These instructions show how to modify a suite to run the `pptransfer` task on the ARCHER2 login nodes and push the data across to JASMIN from ARCHER2 `/work` disk.  

**Note 1:** Instructions cannot cover all possible suite setup combinations so you may need to adjust them accordingly. For example, tasks may be named slightly differently or inherit differently.

**Note 2:** In order to use `hpxfer[1-2].jasmin.ac.uk` you need to have requested access to the High Performance Data Transfer service via the JASMIN accounts portal.

**Note 3:** Although the full ARCHER2 system does have serial nodes, it is not possible to ssh to JASMIN from them.  Whilst the ARCHER2/JASMIN teams work towards a permanent solution, for the time being we need to continue running data transfers on the login nodes.

## Suite Changes

Note, see **u-bs251-archer2** for a complete working postproc and pptransfer example suite.

In the rose suite editor go to *"postproc -> Post processing - common settings"*:

*  In panel *"Archer Archiving"* change **archive_root_path** to be a directory on the `/work` disk \\
For example; `/work/n02/n02/<username>/archive` where `<username>` is your ARCHER2 username.  \\
This will be a temporary area to stage your data before transfer to JASMIN.

* In panel *"JASMIN Transfer"*:
  * Set **transfer_type** to `Push`
  * Set **remote_host** to `hpxfer1.jasmin.ac.uk` \\
  (If you do not have access to `hpxfer1.jasmin.ac.uk` use either `xfer1.jasmin.ac.uk` or `xfer2.jasmin.ac.uk` instead.)
  * Set **gridftp** to `false`

Ideally you will have ARCHER2 specific file, `~/roses/<SUITEID>/site/archer2.rc` 

* Replace the line `host = dtn02.rdf.ac.uk` with `host = loginX.archer2.ac.uk`. Where X is either 1,2,3 or 4.

Ideally, `archer2.rc` will include sections `[[POSTPROC_RESOURCE]]` and `[[PPTRANSFER_RESOURCE]]` (that may not be precisely the case, but what follows should guide you to configure your suite):

Make your suite look like this:
~~~
    [[POSTPROC_RESOURCE]]
        inherit = HPC_SERIAL
        pre-script = """module load postproc
                        module list 2>&1
                        ulimit -s unlimited
                     """
                     
    [[PPTRANSFER_RESOURCE]]
        inherit = POSTPROC_RESOURCE
        [[[job]]]
            batch system = background
        [[[remote]]]
            host = loginX.archer2.ac.uk      <== replace X with a number between 1 & 4 to pick a specific login node
~~~

If there is no `[[POSTPROC_RESOURCE]]` section, make `[[PPTRANSFER_RESOURCE]]` look like this:
~~~
    [[PPTRANSFER_RESOURCE]]
        inherit = HPC_SERIAL
        pre-script = """module load postproc
                        module list 2>&1
                        ulimit -s unlimited
                     """
       [[[job]]]
            batch system = background
        [[[remote]]]
            host = loginX.archer2.ac.uk      <== replace X with a number between 1 & 4 to pick a specific login node
~~~

**Note:** Since we are currently having to run the transfers from a login node it is essential that they are submitted to a specific login node (e.g. login3.archer2.ac.uk) so that the cylc polling works.  Be aware that you may need to switch login node part way through a run if the node you have specified is taken out of service.

## Setup required on ARCHER2

You now need to setup `ssh-agent` on each ARCHER2 login node to be able to login to `hpxfer1.jasmin.ac.uk` non-interactively.

 1. Login to ARCHER2 \\
   (Note: this need to be from somewhere other than PUMA) \\
   \\
   There are four login nodes at ARCHER2 (login[1-4].archer2.ac.uk), one of which is invariably not accessible. To login into node X:
~~~
ssh loginX.archer2.ac.uk
~~~

 2. Add the following lines to your `~/.bash_profile`:
~~~
# ssh-agent setup on login nodes
. ~/.ssh/ssh-setup
~~~

 3. Copy the `~/.ssh/ssh-setup` script.
~~~
$ cp /work/y07/shared/umshared/um-training/ssh-setup ~/.ssh
~~~

 4. Copy the ssh-key you use to access JASMIN to `~/.ssh` directory (e.g. `id_rsa_jasmin`)

 5. Add the following to your `~/.ssh/config` file (create one if it doesn't already exist):
~~~
Host xfer?.jasmin.ac.uk hpxfer?.jasmin.ac.uk
User <jasmin_username>
IdentityFile ~/.ssh/<jasmin_key>
ForwardAgent no
~~~
 Where `<jasmin_username>` is your JASMIN username and `<jasmin_key>` is the name of your ssh-key. \\
 \\
 **Note:** in order to use `hpxfer1.jasmin.ac.uk` you need to have requested access to the High Performance Data Transfer service via the JASMIN accounts portal.

 6. Logout and then log back in again to start up your ssh-agent.

 7. Run `ssh-add ~/.ssh/<jasmin_key>` where `<jasmin_key>` is the name of your JASMIN ssh-key E.g. `id_rsa_jasmin`. (This is the key you generated when you applied for access to JASMIN). Type in your passphrase when prompted to do so.

 8. You should now be able to login to the required JASMIN transfer node (either `xfer[1-2].jasmin.ac.uk` or the high performance node `hpxfer[1-2].jasmin.ac.uk`) without being prompted for passphrase/password.

 9. Repeat for the remaining login nodes.


## Updating a Running Suite
1. Reload the suite: `rose suite-run --reload`
1. Hold the whole suite, or just the next `pptransfer` task 
1. In the Cylc GUI: Control --> Insert Task(s)… 
1. Set TASK-NAME.CYCLE-POINT=fcm_make_pptransfer.<YYYYMMDDT0000Z>, where <YYYYMMDDT0000Z> is an active cycle point 
1. Leave stop-point=POINT blank 
1. Check the "Do not check if a cycle point is valid or not" box 
1. Insert, and wait for the task to complete. 
1. If nothing happens: You probably typed something incorrectly!  Try again. 
1. In the Cylc GUI: Control --> Insert Task(s)… 
1. Set TASK-NAME.CYCLE-POINT=fcm_make2_pptransfer<YYYYMMDDT0000Z>, where <YYYYMMDDT0000Z> is an active cycle point 
1. Leave stop-point=POINT blank 
1. Check the "Do not check if a cycle point is valid or not" box 
1. Insert, and wait for the task to complete. 
1. Release the held suite/pptransfer task 
