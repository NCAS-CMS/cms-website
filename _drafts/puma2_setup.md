---
layout: page-fullwidth
title: puma2
teaser: Getting setup on PUMA2
---

## Getting setup on PUMA2

***These are draft instructions and are subject to change.***

You will need to do some setup on the new system. 
Please follow the instructions carefully. 
There are several steps, and some subtle differences to the old puma server. 
If you have any difficulties, contact the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk/).

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

### 3. Set up passwordless access to PUMA2

You can set up a passphrase-less ssh-key to access PUMA2, 
so that you don't have to type your password every time.

**Important: You still need to use 2-factor authentication to access the ARCHER2 login nodes, 
with a strong passphrase protecting your ARCHER2 ssh-key**

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

### 4. Setting up your PUMA2 environment 

Some of the setup here is a bit different to PUMA, 
so we recommend you move any exisiting ```.profile

* To setup your environment, copy the standard ```.profile``` and ```.bashrc```. 
  ```
  cd
  cp ~um1/um-training/puma2/.profile .
  cp ~um1/um-training/puma2/.bashrc . 
  ```

* To pick up these settings, logout of PUMA2 and back in again.
  Ignore the warning about `ssh-setup: No such file or directory`. 

* You should be prompted for your MOSRS password, then username.
  (Note that it asks for your **password** first.)
  If the password caching works,  you should see: 
  ```
  Subversion password cached
  Rosie password cached
  ```

### 5. Setting up your ssh agent 

You need to have an ssh-agent running in order to submit jobs to ARCHER2.

These instructions assume your ARCHER2 key is called `~/.ssh/id_rsa_archer2`. 
Replace this with the name of your key. 

#### i. Copy your ARCHER2 ssh-key pair to PUMA2  

***Think about how to do this***

#### ii. Now start up you ssh-agent and add the ARCHER2 key

* Copy the `ssh-setup` script to your `.ssh` directory.

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

***Are we getting users to edit their .ssh/config from old puma, or start a new one?***

* If it doesn't exist, create the file: ```~/.ssh/config```,
  and add the following lines:
  ```
  # ARCHER2 login nodes
  Host ln* 
     IdentityFile ~/.ssh/id_rsa_archer2

  Host *
     ForwardAgent no
  ```

* To test this is working, run:
  ```
  rose host-select archer2
  ```
  It should return one of the login nodes, e.g. ```ln01```.
  If it returns a message like ```[WARN] ln03: (ssh failed)``` then something has gone wrong with the ssh setup.

#### iv. Configure access to JASMIN 

If you want to be able to submit jobs to JASMIN (e.g. for JDMA): 
* Follow the instructions in the "Setup connection to JASMIN sci nodes" section on [this page](https://cms.ncas.ac.uk/unified-model/jdma)
* Replace ```login1``` with ```login2``` in your ```~/.ssh/config``` file, as we can't currently access login1 from puma2. 

### 6. Setting up your ARCHER2 environment 

* If you have not previously run on ARCHER2 before, copy the standard `.profile` to your environment: 
  ```
  cp /work/y07/shared/umshared/um-training/rose-profile ~/.profile
  ```

***The default version of Rose and cylc are the same, 
so you can skip this step if you don't want to mess up your A2 setup.***

The new PUMA2-managed software is under: ```/work/y07/shared/umshared/metomi/bin/cylc```

* To test this, edit your ```.profile```, and replace this line: 
  ```
  . /work/y07/shared/umshared/bin/rose-um-env
  ```
  with this one: 
  ```
  . /work/y07/shared/umshared/bin/rose-um-env-puma2
  ```
