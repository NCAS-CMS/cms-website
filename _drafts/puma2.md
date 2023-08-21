---
layout: page-fullwidth
title: PUMA2
teaser: PUMA2
---

***These are draft instructions and are subject to change.***

## PUMA2

We are moving to a new server PUMA2, 
hosted at ARCHER2 and jointly managed by CMS and EPCC.
Having PUMA2 co-located with ARCHER2 should make things easier, 
since you will use the same account to access both machines.

Upgrading PUMA also allows us to support new UM infrastructure,
such as cylc-8, which will eventually be controlled by a web interface. 
Unfortunately, the PUMA server we've been using has several limitations
and was only ever meant to be an interim solution after the demise of the old machine. 

## Moving over to PUMA2

The process of moving from PUMA to PUMA2 is as follows: 
* Apply for a PUMA2 account.
* Stop any suites you have running on the old PUMA.
* Copy your files over.
* Set up your PUMA2 environment.
* Set up your ssh connection to ARCHER2 (and JASMIN if required).
* Restart any running suites.

***Maybe just put in a table of contents here?***

Please follow the instructions carefully. 
There are several steps, and some subtle differences to the old puma server. 
If you have any issues, contact the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk/).

***These are draft instructions and subject to change.***

### 1. Stop any suites you have running on PUMA. 

First shutdown any suites you have running on PUMA. 
***You need to wait for any remote tasks to finish*** before moving over, so it's wise to do this first. 
You can restart your suites again on PUMA2 once you have completed the setup - instructions are at the end of this page. 

* You can see which suites you have running with ```cylc gscan```

* To stop a suite, open up the rose suite control GUI with ```rose sgc```
  
* Then in the "Suite" menu, select "Stop Suite", and "Stop after active tasks have finished" (the default).
  Once any running tasks have finished the suite will shutdown. 

You can move on to Steps 2 and 3 whilst waiting for your suites to stop. 

### 2. Apply for an account

(If you don't already have an ARCHER2 account, 
follow [these instructions](https://docs.archer2.ac.uk/quick-start/quickstart-users/#request-an-account-on-archer))

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

If you have been running suites on ARCHER2, you should have an archerum key installed. 
You can this to push files directly from PUMA. 

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
so we don't need to login to PUMA2.   

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

When you login to PUMA2 you will probably get some warnings like: 
```
bash: cylc: command not found...
bash: rose: command not found...
bash: fcm: command not found...
-bash: mosrs-setup-gpg-agent: No such file or directory
```
That's because the location of this software has changed on PUMA2, so you need to update your environment. 

* If you wish to save your old ```.profile```, ```.bashrc``` or ```.bash_profile```
  move these out the way first: 
  ```
  cd
  mv .profile .profile.SAVE
  mv .bashrc .bashrc.SAVE
  mv .bash_profile .bash_profile.SAVE
  ```

* To setup your PUMA2 environment, copy the standard ```.profile``` and ```.bashrc```. 
  ```
  cd
  cp ~um1/um-training/puma2/.profile .
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

### 7. Set up your ssh agent 

You need to have an ssh-agent running in order to submit jobs to ARCHER2.

#### i. Copy your ARCHER2 ssh-key pair to PUMA2  

You may already have this in your ```.ssh``` directory, otherwise you will need to copy it over. 

* From your local system, run: 
  ```
  scp ~/.ssh/<archer-key>* <archer-username>:/home/n02/n02-puma/<archer-username>/.ssh
  ```

#### ii. Now start up you ssh-agent and add the ARCHER2 key

You should alreay have the `ssh-setup` script in your `.ssh` directory, 
and your agent should have been launched when you logged in. 

* Add your ARCHER key to the ssh agent: 
  ```
  ssh-add ~/.ssh/<archer-key>
  ```
  Type your passphrase when prompted

***What if this doesn't work?***

#### iii. Configure access to the ARCHER2 login nodes 

Since we are using our regular ARCHER2 key, and not the archerum key, we need to edit our ssh config file. 

* In your ```.ssh/config``` file delete the following lines:
  ```
  Host login.archer2.ac.uk
  User <archer-username>
  IdentityFile ~/.ssh/id_rsa_archerum
  ``` 

* Replace with these lines:
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

#### iv. (Optional) Configure access to JASMIN 

If you want to be able to submit jobs to JASMIN (e.g. for [data migration to JDMA](https://cms.ncas.ac.uk/unified-model/jdma), 
you need to set up ssh access. 
This assumes you already had JASMIN access on old PUMA. 

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

***Note: the Rose/cylc versions are the same, so could we switch this under the hood for everyone?**

The new PUMA2-managed software is under: ```/work/y07/shared/umshared/metomi/bin/cylc```

* Edit your ```.profile```, and replace this line: 
  ```
  . /work/y07/shared/umshared/bin/rose-um-env
  ```
  with this one: 
  ```
  . /work/y07/shared/umshared/bin/rose-um-env-puma2
  ```
  
### 9. Restarting and running suites

You should now be able to checkout and run suites as before, with the following change: 

* Edit ```site/archer2.rc``` file and replace any lines like this:
  ```
  host = login.archer2.ac.uk
  ```
  with this:
  ```
  host = $(rose host-select archer2)
  ```

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

* To restart a suite:
  ```
  rose suite-run --restart
  ```

## Troubleshooting 

You tried to restart your suite and get the following error: 
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

We have also taken this opportunity to archive some old files and directories. 

## Known issues 

* Code checkouts are slow. 
* You will not be able to view job log files in the cylc GUI for tasks that ran on old PUMA. 
  This is because cylc will try to retrieve the files from the remote host using the old hostname.
  You can still view the logs in your ```cylc-run``` directory on PUMA2 or ARCHER2. 
* The UMUI currently doesn't work. 
* The old UM, NEMO and CICE repositories have not yet been moved over. 
* ```fcm_make_pp``` will have fail because ```fcm:nemo``` is not defined.
  As a work-around, edit ```app/fcm_make_pp/rose-app.conf``` and set: 
  ```
  config_base=/home/n02/n02/annette/moci/postproc_2.4_canari
  ```
