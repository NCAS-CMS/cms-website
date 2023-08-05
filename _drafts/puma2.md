---
layout: page-fullwidth
title: PUMA2
teaser: PUMA2
---

***These are draft instructions and are subject to change.***

## PUMA2

We are moving the PUMA service to a new home at ARCHER2. 
The new server will be called PUMA2 and it will be jointly managed by CMS and EPCC.
Having PUMA2 in the same place as ARCHER2 will make things easier in the long-term, 
as you will use the same account (username, password and ssh key) to access both machines.

We need to upgrade the puma server in order to support new UM infrastructure,
such as cylc-8, which will eventually be controlled by a web interface. 
The puma server we've been using was only ever meant to be an interim solution after the demise of the old machine, 
and it is not suitable as a long-term replacement. 

## Summary of changes 

***Possibly move this somewhere else***

* The ```um``` user account is now ```um1```
* Home directory paths have changed from ```/home/``` to  ```/home/n02/n02/```.
* We access JASMIN via login2.
* The MOSRS password caching scripts are different. 
* The paths to Rose, cylc and FCM are different on PUMA2 and ARCHER2, but the default versions are the same
* We have cylc-8 on PUMA2. You can use the terminal UI.
* Suites need to specify ```host = $(rose host-select archer2)```

## Moving over to PUMA2

***These are draft instructions and are subject to change.***

The process of moving from PUMA to PUMA2 is as follows: 
* Apply for a PUMA2 account.
* Stop any suites you have running on the old PUMA.
* Copy your files over.
* Set up your PUMA2 environment.
* Set up your ssh connection to ARCHER2 (and JASMIN if required).
* Restart any running suites. 

Please follow the instructions carefully. 
There are several steps, and some subtle differences to the old puma server. 
If you have any issues, contact the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk/).

### 1. Apply for an account 

You will need to request a PUMA2 account via SAFE. 

If you don't already have an ARCHER2 account, 
follow [these instructions](https://docs.archer2.ac.uk/quick-start/quickstart-users/#request-an-account-on-archer)

To request access to PUMA2: 
* Login to [SAFE](https://safe.epcc.ed.ac.uk/)
* From the "Login accounts" menu, select your username
* Scroll down near the bottom, and select "Add Machine"
* At the bottom of the next page, under "Machine to join", select "puma2", and click "Join"

You will be sent an email when your PUMA2 account is ready for use. 

### 2. Login to PUMA2

PUMA2 is accessed from the ARCHER2 login nodes, and uses the same username and password. 

* [Login to ARCHER2](https://docs.archer2.ac.uk/quick-start/quickstart-users/#login-to-archer2) as usual.

**Important: We recommend users ***do not forward their ssh-agent*** from their local system, 
as this can cause problems with Rose/cylc job submission.**

* Once you are on the ARCHER2 login nodes, type ```ssh -Y puma2```. Enter your ARCHER2 password when prompted.
  
* You should now be logged into to PUMA2. To go back to the ARCHER2 login nodes, type ```exit```

### 3. Stop any suites you have running on PUMA. 

If you have any suites running on PUMA that you wish to continue on PUMA2, 
stop them now, before copying your files over. 

* To see which suites you have running, run:
```
cylc gscan
```

* Double-click on a suite to launch the suite control GUI, or ```cd``` to the roses directory and run ```rose sgc```. 

* In the "Suite" menu, select "Stop now (restart will follow up on orphaned tasks)".
  This stops the suite, but leaves any running tasks going.

When we restart the suite on PUMA2, cylc will pick up the latest status of each task. 

### 4. Copy over your files 

You might want to have a clear out and only copy over the files you need. 
But make sure to copy over your ```cylc-run``` and ```roses``` directories 
if you have running suites you wish to continue on PUMA2. 

#### Method i: Push from PUMA to ARCHER2 

If you have been running suites on ARCHER2, you should have an archerum key installed. 
You can this to push files directly from PUMA. 

* To check your connection is working, run: 
  ```
  ssh login.archer2.ac.uk
  ```
  This should return:
  ```
  PTY allocation request failed on channel 0
  Comand rejected by policy. Not in authorised list 
  Connection to login.archer2.ac.uk closed.
  ```

Conveniently, the PUMA2 filesystem is cross-mounted on the ARCHER2 login nodes.   

* To move all your files, run: 
  ```
  rsync -a . login.archer2.ac.uk:/home/n02/n02-puma/<archer-username>
  ```
  This might take a little while if you have lots of files.

**Note: I'm not sure if it's entirely safe to copy over all the hidden files, 
so let's see if this works. Otherwise use --exclude '.*'**

#### Method ii: Pull from PUMA2

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

* Next, create a file called ```~/.ssh/config```, and add the following lines: 
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

* If you wish to save your ```.profile```, ```.bashrc``` or ```.bash_profile``` from the old PUMA, 
  move these out the way first, and copy in anything you need afterwards. 
  ```
  cd
  cp .profile .profile.SAVE
  cp .bashrc .bashrc.SAVE
  cp .bash_profile .bash_profile.SAVE
  ```

* To setup your PUMA2 environment, copy the standard ```.profile``` and ```.bashrc```. 
  ```
  cd
  cp ~um1/um-training/puma2/.profile .
  cp ~um1/um-training/puma2/.bashrc . 
  ```

* To pick up these settings, logout of PUMA2 and back in again.
  Ignore the warning about `ssh-setup: No such file or directory`. 

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

* From your local system, run: 
  ```
  scp ~/.ssh/<archer-key>* <archer-username>:/home/n02/n02-puma/<archer-username>/.ssh
  ```

#### ii. Now start up you ssh-agent and add the ARCHER2 key

* On PUMA2, copy the `ssh-setup` script to your `.ssh` directory.

  ```
  cp ~um1/um-training/setup/ssh-setup ~/.ssh
  ```

* Log out of PUMA2 and back in again to start the ssh-agent. You should see:
  ```
  Initialising new SSH agent...
  ```
  
* Add your ARCHER key to the ssh agent: 
  ```
  ssh-add ~/.ssh/id_rsa_archer2
  ```
  Type your passphrase when prompted

#### iii. Configure access to the ARCHER2 login nodes 

You need to change how we ssh to ARCHER2

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
  IdentityFile ~/.ssh/id_rsa_archer2
  ```

* To test this is working, run:
  ```
  rose host-select archer2
  ```
  It should return one of the login nodes, e.g. ```ln01```.
  If it returns a message like ```[WARN] ln03: (ssh failed)``` then something has gone wrong with the ssh setup.

#### iv. Configure access to JASMIN 

If you want to be able to submit jobs to JASMIN (e.g. for JDMA), you need to set up ssh access. 
Note that we need to use JASMIN login2. 

* Add the following lines to the top of your ```.ssh/config``` file,
  editing for your JASMIN username and the path to your JASMIN key:
  ````
  # JASMIN
  Host login2
  Hostname login2.jasmin.ac.uk
  User <jasmin_username> 
  IdentityFile ~/.ssh/<jasmin-ssh-key>
  ForwardAgent yes
  ControlMaster auto
  ControlPath /tmp/ssh-socket-%r@%h-%p
  ControlPersist yes

  Host sci? cylc1
  Hostname %h.jasmin.ac.uk

  Host sci* cylc*
  User <jasmin_username>
  IdentityFile ~/.ssh/<jasmin-ssh-key>
  ForwardAgent yes
  ProxyCommand ssh -Y login2 -W %h:%p
  ControlMaster auto
  ControlPath /tmp/ssh-socket-%r@%h-%p
  ControlPersist yes
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

### 8. Set up your ARCHER2 environment 

* If you have not previously run on ARCHER2 before, copy the standard `.profile` to your environment: 
  ```
  cp /work/y07/shared/umshared/um-training/rose-profile ~/.profile
  ```

***Note: the Rose/cylc versions are the same, so we should be able to switch this already??**

The new PUMA2-managed software is under: ```/work/y07/shared/umshared/metomi/bin/cylc```

* Edit your ```.profile```, and replace this line: 
  ```
  . /work/y07/shared/umshared/bin/rose-um-env
  ```
  with this one: 
  ```
  . /work/y07/shared/umshared/bin/rose-um-env-puma2
  ```
  
### 9. Restart your suites 

You should be able to checkout and run suites as before.

Changes required: 

* In your ```site/archer2.rc``` file replace lines line this:
  ```
  host = login.archer2.ac.uk
  ```
  with this:
  ```
  host = $(rose host-select archer2)
  ```




