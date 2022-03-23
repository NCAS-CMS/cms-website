---
layout: page-fullwidth
title: PUMA
subheadline: 
teaser: PUMA (Providing Unified Model Access) is the service setup by NCAS-CMS to provide the UK research community with centralised access to the UM on ARCHER2 and other national HPCs.
permalink: /puma/
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

The PUMA service runs on hardware located at the University of Reading.  It hosts mirrors of the Met Office Science Repositories and provides access to Rose & Cylc enabling submission of model simulations to ARCHER2 and other HPCs/clusters.  The PUMA service has several hundred registered users.  It also hosts the KPP repository which is accessible to the global community.

{% include alert info="March 2022: <br> PUMA is currently replaced with a temporary server pumatest.nerc.ac.uk, whilst we wait for a new server to be procured and configured." %}

## Request an account on PUMA

Please email the CMS Team to ask for the PUMA registration link or raise a ticket on our modelling helpdesk.

If you will only be running suite on Monsoon2 then you DO NOT need a PUMA account.

## Connecting to PUMA 

Both an SSH key pair, protected by a passphrase, **and** a password are required to login onto PUMA. Interactive access is achieved using SSH, either directly from a command-line terminal or using an SSH client. 
</div><!-- /.medium-8 -->
</div><!-- /.row -->
#### Windows

A typical Windows installation will not include a terminal client.  We recommend Windows users download and install MobaXterm to access PUMA. JASMIN website has some nice instructions on using [MobaXterm](https://help.jasmin.ac.uk/article/4832-mobaxterm).

#### Linux and MacOS

Linux distributions and MacOS include a terminal application that can be used for SSH access.

`ssh-agent` is a utility that stores private keys and makes them available to other software that use the SSH protocol to connect to remote clients.  There are two stages to loading your private keys into `ssh-agent`; starting the agent and then loading your private key.

~~~
$ eval $(ssh-agent -s)
$ ssh-add ~/.ssh/id_rsa_puma
Enter passphrase for /home/ros/.ssh/id_rsa_puma:
Identity added: /home/ros/.ssh/id_rsa_puma (/home/ros/.ssh/id_rsa_puma)
~~~

When you run the `ssh-add` command you will be prompted to enter the passphrase that you specified when generating the SSH key pair.

You can test whether your key has been loaded by using the `-l` option to list the currently loaded keys in your agent:
~~~
$ ssh-add -l
4096 SHA256:oi+hEYR+HfHN1mAIEOyDejt09LCAUmWIXL9ndfFbyaE /home/ros/.ssh/id_rsa_puma (RSA)
~~~

This confirms that the key is loaded and ready for use.

## Logging into PUMA

Use the following command from the terminal window to login to PUMA:
~~~
ssh -Y username@puma.nerc.ac.uk
~~~
You will first be prompted for the passphrase associated with your SSH key pair.  Once you have entered this passphrase successfully, you will then be prompted for your machine account password.

When you first login to PUMA you will be prompted to change your initial password.  Thereafter, if you wish to change your password again, you can do so using the `passwd` command.  Passwords should be at least 8 characters long, contain a mixture of letters and numbers and at least 1 non-alphanumeric character.

## Shells

PUMA is running CentOS.  The login shell is the Bash shell (bash)

## Transferring Files

File transfer to and from PUMA can be achieved via `scp` or `sftp`. For example:
~~~
userid1@host$ scp filename.tar userid2@puma.nerc.ac.uk:.
userid2@puma.nerc.ac.uk's password:
filename.tar 100% |*******************************| 5170 00:00
userid1@host$
~~~

## Software

#### Editors

The following text editors are available on PUMA: `vi`, `emacs` and `nedit`.

#### Rose/Cylc

Rose, Cylc & FCM are available on PUMA.  Further details can be found on the [Rose/Cylc pages](#TODO).

#### UMUI

To start up the UMUI simply issue the command:

`puma$ umui`

## System Maintenance

Details of system maintenance, planned outages as well as informative notices will be sent to the PUMA users' email list. You will automatically be added to this mailing list when your PUMA account is activated. Whilst it is possible to unsubscribe yourself from this mailing list we advise that you DO NOT do so otherwise you will miss out on important announcements affecting PUMA. Only the PUMA systems team can post to this mailing list.



