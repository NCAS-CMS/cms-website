---
layout: page-fullwidth
subheadline: PUMA2
title: PUMA2
permalink: /puma2/
---

The PUMA2 service was setup by NCAS-CMS to provide the UK research community with centralised access to the UM on Cirrus and other national HPCs. 
It hosts mirrors of the Met Office Science Repositories and provides access to Rose & Cylc enabling submission of model simulations to Cirrus and other machines. 

PUMA2 is hosted at Edinburgh and jointly managed by CMS and EPCC. PUMA2 access is managed through the SAFE system. 

## Applying for an account

To request a PUMA2 account. 
* Login to [SAFE](https://safe.epcc.ed.ac.uk/)
* From the "Login accounts" menu, select your username
* Scroll down near the bottom, and select "Add Machine"
* At the bottom of the next page, under "Machine to join", select "puma2", and click "Join"

You will be sent an email when your PUMA2 account is ready for use. 

## Accessing PUMA2

PUMA2 is accessed from the Cirrus login nodes, and you will use the same username and ssh-key that you use to access Cirrus.

* [Login to Cirrus](https://www.cirrus.ac.uk/) as usual.

**Important:** We recommend users ***do not forward their ssh-agent*** from their local system, 
as this can cause problems with Rose/cylc job submission.

* Once you are on the Cirrus login nodes, type ```ssh -Y puma2```. Enter your Cirrus password when prompted.
  
* You should now be logged into PUMA2.

## Default login scripts

Some sample login scripts such as `.bashrc` and `.bash_profile` can be found on PUMA2 here; 

* `/home/n02/n02/um1/um-training/puma2/`.

## Connecting to PUMA2 via Cirrus

The best way to setup connection to PUMA2 via Cirrus is to use port-forwarding from your local machine/laptop. This setup is also necessary in order to use the cylc 8 web UI.

Edit the ~/.ssh/config file on your local machine so that the Cirrus and PUMA2 sections contain:

```
# PUMA2
Host puma2
User <username>
IdentityFile ~/.ssh/<your-cirrus-ssh-key>
ProxyJump cirrus
ForwardX11 yes

# Cirrus
Host cirrus
Hostname login.cirrus.ac.uk
User <username>
IdentityFile ~/.ssh/<your-cirrus-ssh-key>
ForwardX11 yes
```

You should now be able to type ssh puma2 on your laptop/local machine and land directly on PUMA2. You may or may not be asked for your cirrus key passphrase depending on your setup.



## Running workflows on Cirrus 

Follow the [setup instructions](https://ncas-cms.github.io/um-training/getting-setup-selfstudy.html) in our online training to configure your environment to run workflows on Cirrus.

For more information, see our documentation: 
* [Unified Model]({{ '/unified-model/'| relative_url }})
* [Rose/cylc]({{ '/rose-cylc/'| relative_url }})
* [Cylc 8]({{ '/cylc8/'| relative_url }})
* [UMUI](umui)

## PUMA2 files

You can access your PUMA2 home directory on Cirrus via:
```
/home/n02/n02-puma2/<username>/
```
