---
layout: page-fullwidth
subheadline: PUMA2
title: Transition to PUMA2 
teaser: Here you will find instructions for getting setup on our new server PUMA2, including copying data and moving over live suites. 
permalink: /puma2/
---

<div class="row">
<div class="medium-4 medium-push-8 columns" markdown="1">
<div class="panel radius" markdown="1">
**Table of Contents**
{: #toc }
*  TOC
{:toc}
</div><!-- /.panel -->
</div><!-- /.medium-4 -->

<div class="medium-8 medium-pull-4 columns" markdown="1">

{% include alert info="These are draft instructions and are subject to change." %}


## The PUMA service 

The PUMA service was setup by NCAS-CMS to provide the UK research community with centralised access to the UM on ARCHER2 and other national HPCs. 
It hosts mirrors of the Met Office Science Repositories and provides access to Rose & Cylc enabling submission of model simulations to ARCHER2 and other HPCs/clusters.

## PUMA2

We are transitioning to a new server PUMA2, hosted at ARCHER2 and jointly managed by CMS and EPCC. 
Having PUMA2 co-located with ARCHER2 will make things easier for users, 
since the same account will be used for both machines.

Upgrading PUMA also allows us to support new UM infrastructure,
such as cylc-8, which will eventually be controlled by a web interface. 
Unfortunately, the old PUMA has several limitations
and was only ever meant to be an interim solution. 

## Moving over to PUMA2

Users will be invited to move over in batches to help CMS manage the transition. 

To use PUMA2, you will need to move over your files from old PUMA,
and then setup your account on the new system. 
This involves making some changes to your user environment, 
and configuring an ssh-agent to run jobs on ARCHER2 and JASMIN. 

Please follow the instructions carefully. 
There are several steps, and some subtle differences to the old PUMA server. 
If you have any issues, contact the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk/).

New users can skip sections 1, 4 and 10. 

### 1. Stop any suites you have running on PUMA. 

**Important: Follow this section carefully to continue running your suites on PUMA2.**

First shutdown any suites you have running on PUMA. 
***You need to wait for any remote tasks to finish*** before moving over. 
You can restart your suites again on PUMA2 once you have completed the setup - instructions are in the final step. 

* You can see which suites you have running with ```cylc gscan```

* Double-click on any running suites to bring up the suite control GUI. 
  
* Then in the "Suite" menu, select "Stop Suite", and ***"Stop after active tasks have finished"*** (the default).
  Once any running tasks have finished the suite will shutdown. 

You can move on to Steps 2 and 3 whilst waiting for your suites to stop. 

### 2. Apply for an account

If you don't already have an ARCHER2 account, 
follow [these instructions](https://docs.archer2.ac.uk/quick-start/quickstart-users/#request-an-account-on-archer)

You will need to request a PUMA2 account via SAFE. 
* Login to [SAFE](https://safe.epcc.ed.ac.uk/)
* From the "Login accounts" menu, select your username
* Scroll down near the bottom, and select "Add Machine"
* At the bottom of the next page, under "Machine to join", select "puma2", and click "Join"

You will be sent an email when your PUMA2 account is ready for use. 

### 3. Login to PUMA2

PUMA2 is accessed from the ARCHER2 login nodes, and you will use the same username and password. 

* [Login to ARCHER2](https://docs.archer2.ac.uk/quick-start/quickstart-users/#login-to-archer2) as usual.

**Important: We recommend users ***do not forward their ssh-agent*** from their local system, 
as this can cause problems with Rose/cylc job submission.**

* Once you are on the ARCHER2 login nodes, type ```ssh -Y puma2```. Enter your ARCHER2 password when prompted.
  
* You should now be logged into PUMA2. To go back to the ARCHER2 login nodes, type ```exit```

### 4. Copy over your files 

**Important: You must wait for your suites to shutdown properly before moving your files over**

You might want to have a clear out and only copy over the files you need. 
But make sure to copy over your ```cylc-run``` and ```roses``` directories 
if you have running suites you wish to continue on PUMA2. 

#### Preferred method: Push from PUMA to ARCHER2 

If you have been running suites on ARCHER2, you should have an ```archerum``` key installed. 
You can use this to push files directly from PUMA. 

* Login to the old PUMA

* To check your connection to ARCHER2 is working, run: 
  ```
  ssh login.archer2.ac.uk
  ```
  This should return:
  ```
  PTY allocation request failed on channel 0
  Comand rejected by policy. Not in authorised list 
  Connection to login.archer2.ac.uk closed.
  ```

Conveniently, the PUMA2 filesystem is cross-mounted on the ARCHER2 login nodes, 
so you don't need to login to PUMA2.   

* To move all your files over, run: 
  ```
  rsync -a . login.archer2.ac.uk:/home/n02/n02-puma/<archer-username>
  ```
  This might take a while if you have lots of files.

#### Alternative method: Pull from PUMA2

If you don't have an archerum key installed, you will not be able to access ARCHER2 from PUMA, 
so you will need to login to PUMA2 and pull your files over. 

### 5. Set up passwordless access to PUMA2

You can set up a passphrase-less ssh-key to access PUMA2, 
so that you don't have to type your password every time.

* From the ARCHER2 login nodes, type 

  ```
  ssh-keygen -t rsa -f ~/.ssh/id_rsa_puma2
  ```

* At the prompt, press enter for an empty passphrase.

* Copy the key over to PUMA2:
  ```
  ssh-copy-id -i ~/.ssh/id_rsa_puma2 puma2
  ```
  Type in your ARCHER2 password when prompted. 

* Next, create a file called ```~/.ssh/config``` (if it doesn't already exist), and add the following lines: 
  ```
  Host puma2
  IdentityFile ~/.ssh/id_rsa_puma2
  ForwardX11 yes
  ```

* Test it works by typing ```ssh puma2```.
  You should not be prompted for your password.
  Note that this should have set up X11 forwarding, so you no longer need the `-Y`.

**Important: You should not use a passphrase-less key to access the ARCHER2 login nodes, as this is a serious security risk**

### 6. Set up your PUMA2 environment 

When you next login to PUMA2 after copying your files over from PUMA, 
you will probably get some warnings like: 
```
bash: cylc: command not found...
bash: rose: command not found...
bash: fcm: command not found...
-bash: mosrs-setup-gpg-agent: No such file or directory
```
That's because the location of this software has changed on PUMA2, so you need to update your environment. 

* If you wish to save your old ```.profile```, ```.bashrc``` or ```.bash_profile```,
  move these out of the way first: 
  ```
  cd
  mv .profile .profile.SAVE
  mv .bashrc .bashrc.SAVE
  mv .bash_profile .bash_profile.SAVE
  ```

* To setup your PUMA2 environment, copy the standard ```.bash_profile``` and ```.bashrc```. 
  ```
  cd
  cp ~um1/um-training/puma2/.bash_profile .
  cp ~um1/um-training/puma2/.bashrc . 
  ```

* To pick up these settings, logout of PUMA2 and back in again.

* You should be prompted for your MOSRS password, then username.
  (Note that it asks for your **password** first.)
  If the password caching works, you should see: 
  ```
  Subversion password cached
  Rosie password cached
  ```

  If you get a warning about ```~/.ssh/ssh-setup``` not being found, ignore this for now. 

### 7. Set up your ssh agent 

In order to submit jobs to ARCHER2 and JASMIN, 
you need to have an ssh-agent running with your ssh-keys for each machine added. 

#### i. Copy your ARCHER2 ssh-key pair to PUMA2  

Your ARCHER2 key is the one that you use to ssh into the ARCHER2 login nodes. 

**Note: If you have already been running suites on ARCHER2 from old PUMA, 
you will also have an ```archerum``` key,
but we recommend you no longer use this, 
just to simplify the number of keys in your workflow.**

You need to copy both the public and private keys into your ```.ssh/``` directory on PUMA2. 

* From your local system, run: 
  ```
  scp ~/.ssh/<archer-key>* login.archer2.ac.uk:/home/n02/n02-puma/<archer-username>/.ssh
  ```

#### ii. New users only: Start up your ssh agent

If you are not moving over from the old PUMA, or you were not setup to run suites, 
then you need to do an extra bit of setup to launch your ssh-agent. 

* First copy the ```ssh-setup``` script to your ```.ssh/``` directory. 

  ```
  cp ~um1/um-training/setup/ssh-setup ~/.ssh
  ```

* Now log out of PUMA2 and back in again to start up your ssh-agent.
  You should see the following message:
  ```
  Initialising new SSH agent...
  ```

#### iii. Add the ARCHER2 key

You should have the ```ssh-setup``` script in your ```.ssh``` directory, 
and your agent should have been launched when you logged in. 

* Add your ARCHER2 key to the ssh agent: 
  ```
  ssh-add ~/.ssh/<archer-key>
  ```
  Type your passphrase when prompted

#### iv. Configure access to the ARCHER2 login nodes 

You need to edit your ssh config file to point to your ARCHER2 key. 
If you were previously running on PUMA, 
you will need to replace any lines referring to your archerum key. 

* If you have lines like these in your ```.ssh/config```, file delete them:
  ```
  Host login.archer2.ac.uk
  User <archer-username>
  IdentityFile ~/.ssh/id_rsa_archerum
  ``` 

* Add these lines instead:
  ```
  # ARCHER2 login nodes
  Host ln* 
  IdentityFile ~/.ssh/<archer-key>
  ```

* To test this is working, run:
  ```
  rose host-select archer2
  ```
  It should return one of the login nodes, e.g. ```ln01```.
  If it returns a message like ```[WARN] ln03: (ssh failed)``` then something has gone wrong with the ssh setup.

#### v. (Optional) Configure access to JASMIN 

If you want to be able to submit jobs to JASMIN, e.g. for [data migration to JDMA](https://cms.ncas.ac.uk/unified-model/jdma), 
you need to set up ssh access. 

These instructions assume you already had JASMIN access on PUMA. 
If you are doing this for the first time, follow [these instructions](https://cms.ncas.ac.uk/unified-model/jdma#setup-connection-to-jasmin-sci-nodes).  

* Edit your ```.ssh/config``` file and replace ```login1``` with ```login2```, e.g.
  ````
  # JASMIN
  Host login2
  Hostname login2.jasmin.ac.uk
  ...
  ProxyCommand ssh -Y login2 -W %h:%p
  ...
  ````
  
* Add your JASMIN ssh-key to your ssh-agent:
  ```
  ssh-add ~/.ssh/<jasmin-ssh-key>
  ```

* Test you can connect to JASMIN:
  ```
  ssh sci3.jasmin.ac.uk
  ```
  
You should now be logged into the JASMIN sci node without prompt for your JASMIN passphrase. 
If this hangs, double check you don't have any instances of ```login1``` in your ```.ssh/config```. 

### 8. Set up your ARCHER2 environment 

You now need to setup your ARCHER2 environment to point to the new installations 
of Rose, cylc and FCM under: ```/work/y07/shared/umshared/metomi/bin/cylc```

Note: the software versions are the same as before, 
but we have changed the management process to be compatible with PUMA2. 

#### Existing users 

* Login to ARCHER2.

* Edit your ```.profile``` or ```.bash_profile```, and replace this line: 
  ```
  . /work/y07/shared/umshared/bin/rose-um-env
  ```
  with this one: 
  ```
  . /work/y07/shared/umshared/bin/rose-um-env-puma2
  ```

#### New users

* Login to ARCHER2.

* Copy the standard profile into your account:
  ```
  cp /work/y07/shared/umshared/um-training/rose-profile ~/.bash_profile
  ```

* Change the permissions on your ```/home``` and ```/work``` directories to enable the NCAS-CMS team to help with any queries:
  ```
  chmod -R g+rX /home/n02/n02/<your-username>
  chmod -R g+rX /work/n02/n02/<your-username> 
  ```
  
### 9. Update suites to run on PUMA2

You should now be ready to checkout and run suites on PUMA2! 
The final thing to do is make a few changes to the suites themselves. 

ARCHER2 jobs are submitted via the login nodes using ```rose host-select```. 

* Edit ```site/archer2.rc``` file and replace any lines like this:
  ```
  host = login.archer2.ac.uk
  ```
  with this:
  ```
  host = $(rose host-select archer2)
  ```

You may also need to make a few other changes: 

* If anything in your suite points to a local directory like ```/home/<user>``` then you will need to change this path to ```/home/n02/n02/<user>```. 

* If you are using slack alerts, you need to force the ```bin/notify.py``` script to pick up the python3 libraries first.
  Edit the first few lines to look like the following:
  ```
  #!/home/n02/n02/fcm/metomi/conda/mambaforge/bin/python
  
  import sys
  sys.path.insert(0,'/home/n02/n02/fcm/metomi/conda/mambaforge/lib/python3.10')
  
  import argparse
  import http
  import json
  import urllib3
  ```

### 10. Restart any previously running suites. 

You need to pick up the suite changes you have made. 

* Restart by running:
  ```
  rose suite-run --restart
  ```

## Troubleshooting 

Below are some errors that might occur when moving suites over from PUMA. 
Please check you have followed the instructions correctly. 
If you have any other issues, contact the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk/).

### Connection timed out error 

Running or restarting a suite gives the following error: 

```
[FAIL] ssh -oBatchMode=yes -oStrictHostKeyChecking=no -oConnectTimeout=8 -n login.archer2.ac.uk env\ ROSE_VERSION=2019.01.3\ CYLC_VERSION=7.8.12\ bash\ -l\ -c\ \'\"$0\"\ \"$@\"\'\ rose\ suite-run\ -vv\ -n\ u-bz764\ --run=run\ --remote=uuid=b330b450-6f0d-48fd-8689-cd8d2b51f312,now-str=20230904T095548Z # return-code=255, stderr=
[FAIL] ssh: connect to host login.archer2.ac.uk port 22: Connection timed out
```

* Make sure you have ```host = $(rose host-select archer2)``` in the ```site/archer2.rc``` file.

* If you have restarted the suite, make sure you restarted with ```rose suite-run --restart``` in order to pick up any changes. 

### Suite appears to be running error

Restarting a suite gives this: 

 ```
 [FAIL] Suite "u-cs488" appears to be running:
 [FAIL] Contact info from: "/home/n02/n02/annette/cylc-run/u-cs488/.service/contact"
 [FAIL]     CYLC_SUITE_HOST=pumanew.novalocal
 [FAIL]     CYLC_SUITE_OWNER=annette
 [FAIL]     CYLC_SUITE_PORT=43041
 [FAIL]     CYLC_SUITE_PROCESS=15885 python2 /home/fcm/cylc-7.8.12/bin/cylc-run u-cs488
 [FAIL] Try "cylc stop 'u-cs488'" first?
 ```

 * First check the suite is not actually still running on old PUMA. 

 * If it is still running, shut the suite down and re-sync the cylc-run directory for that suite:
   ```
   rysnc -a --delete ~/cylc-run/<suite-id> login.archer2.ac.uk:/home/n02/n02-puma/<archer-username>/cylc-run
   ```
 
  * Then try restarting.

  * If you still get an error, or the suite is not still running on old PUMA,
    delete the ```.service/contact``` file mentioned in the error message. 

### Tasks not updating 

If you shut down the suite without waiting for active tasks to finish, 
the suite will not be able to pick up the task status since it can't connect to the host the tasks 
ran on (login.archer2.ac.uk).

* In the suite log you will see errors like this. 

```
ssh: connect to host login.archer2.ac.uk port 22: Connection timed out
```

* You should be able to recover by manually resetting the task status once the tasks have finished. New tasks should then be triggerd and run correctly.
  
## Summary of changes 

Some of the differeneces between PUMA and PUMA2

* Home directory paths have changed from ```/home/``` to  ```/home/n02/n02/```.
* Suites need to specify ```host = $(rose host-select archer2)```.
* The MOSRS password caching scripts are different.
* The paths to Rose, cylc and FCM are different on PUMA2 and ARCHER2, but the default versions are the same. 
* The ```um``` user account is now ```um1```.
* JASMIN can only be accessed by login2.
* We have cylc-8 on PUMA2. You can use the terminal UI. You should also be able to use the web GUI with port forwarding.
* Emacs works.
* Cylc graph works. 
* Some old files and directories have been archived. Let us know if you think we've archived something that is still in use. 

## Known issues 

* Code checkouts are slow. 
* You will not be able to view job log files in the cylc GUI for tasks that ran on old PUMA. 
  This is because cylc will try to retrieve the files from the remote host using the old hostname.
  You can still view the logs in your ```cylc-run``` directory on PUMA2 or ARCHER2. 
* The UMUI currently doesn't work. 
