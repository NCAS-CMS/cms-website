---
title: Single Column Model
teaser: The Single Column Model (SCM) is a research tool which is used mainly to test/develop the UM physics code. A SCM represents a single atmospheric column at a grid-point in a General Circulation Model (GCM).
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

The Met Office Single Column Model is described in [​UMDP C09](https://code.metoffice.gov.uk/doc/um/latest/papers/umdp_C09.pdf) on the Met Office Science Repository Service (login required). 

The Met Office Single Column Model (SCM) is part of the UM code. At the Met Office it is run on local desktop PCs. This has Rose, Cylc and FCM together with GCOM and the UM shared library (shumlib). NCAS-CMS has the SCM running locally and also using the Met Office's VM (see [below](#TODO)).

SCM suites can be found by starting up the Rosie client running `rosie go`.  From Rosie, search for *“SCUM Template”* this should provide a list of base SCM jobs. All SCM template jobs will have *“SCUM Template [vn]”* in the project field.

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

## Using the Met Office's Virtual Machine to run the SCM

The Single Column Model (SCM) can be easily run inside the Met Office's UM Virtual Machine (VM). For full details of the VM, please see the [​Virtual Machine Guide](https://code.metoffice.gov.uk/doc/um/latest/papers/umdp_X10.pdf) and the associated github repository at ​https://github.com/metomi/metomi-vms

The VM should be run on a system where the user is able to install third party software. In can be run using a linux or windows host, but only the former is supported by CMS. In both cases, Virtualbox and Vagrant are required. Please see the github page for full details on these software packages. Access to [MOSRS](https://code.metoffice.gov.uk) is required. The local directory where the VM was started is mounted as `/vagrant` inside the VM, so files cane be copied to it. It is also possible to `ssh` out of the VM.

### Installation of the VM on Linux
* Install virtualbox and vagrant using local package manager.
  
  
  
* Clone git repo:

   `git clone https://github.com/metomi/metomi-vms.git` <br>
   `cd metomi-vms`
   
* Edit `Vagrantfile.ubuntu-1804` and remove desktop from

  `config.vm.provision :shell, path: "install.sh", args: "ubuntu 1804 desktop mosrs"`
  
  so it looks like

  `config.vm.provision :shell, path: "install.sh", args: "ubuntu 1804 mosrs"`
  
  and remove the line

  `v.gui = true`
  
 * Start the VM with

   `vagrant up`
   
 * Have a coffee while it builds. When it completes, you should now be able to log onto the VM with

   `vagrant ssh`
   
   You will be asked for your MOSRS password and username (in the order).
   
* While logged onto the VM, complete the installation with

  `sudo apt-get install xauth`
  
  and log out and back on again.
  
* The VM is started with `vagrant up`, accessed by `vagrant ssh`, halted with `vagrant halt` and deleted with `vagrant destroy`

### Installation of VM on Windows
* Install Virtualbox and Vagrant

* Download and install git for windows. [​https://gitforwindows.org/](https://gitforwindows.org) Open a command window and

  `git clone https://github.com/metomi/metomi-vms.git`
  
  and cd in the metomi-vms directory
  
* Build the VM with

  `vagrant up`
  
  A Virtualbox window will appear, but ignore this. Have a coffee while it builds.
  
* Start the VM with
 
  `vagrant up`
  
  A window will appear with the VM and a terminal window open. You will be asked for your MOSRS password and username (in the order).

### Preparation of the UM on the VM

Note: the following assumes that UM vn11.3 is required, if a different version is needed, replace 11.3 with that version number.

* Install addition software packages.

  `sudo install-um-extras -v 11.3`
  
* Install additional UM software.

  `um-setup -s fcm:shumlib.x_tr@um11.3`
  
* Install UM data

  `install-um-data`
  
* Install UM Metadata

  `install-rose-meta`
  
* Install UM vn11.3

  `fcm checkout fcm:um.x/trunk@vn11.3 UM11.3` <br>
  `cd UM11.3` <br>
  `rose stem --group=install -S CENTRAL_INSTALL=true`
  
  This will start a rose stem suite to install various input files. The UM installation is now complete.

### Running the SCM
* Start Rosie

  `rosie go &`
  
* Set up the MOSRS repo by clicking on `Edit->Data source` and selecting the Met Office's repo.

* Search for `u-br462` and make a copy.

* Load the job, and run the suite.