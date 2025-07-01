---
title: Migration of UM Data to JASMIN Elastic Tape
teaser: Instructions on how to add the JDMA app to a UM Suite to enable migration of model data to JASMIN Elastic Tape as part of the UM Workflow. 
permalink: '/unified-model/jdma'
---
These instructions assume that your suite is already setup to use the correct version of Postproc. See the [Post-Processing page]({{site.baseurl}}/unified-model/postproc).

## Setup and initialise JDMA on JASMIN
Before you can use the JDMA to migrate data to Elastic Tape you must install the jdma client on JASMIN and initialise some user settings.
 
1. Install JDMA client software:
    * Login to a JASMIN sci machine
    * Create a virtual environment in your home directory:  
      `python3 -m venv ~/jdma_venv`
    * Activate the virtual environment:  
      `source ~/jdma_venv/bin/activate`
    * Install the jdma client into the virtualenv:  
      `pip install git+https://github.com/cedadev/jdma_client`

2. Follow instructions in the [Setting up the user, user settings and user info](https://cedadev.github.io/jdma_client/docs/build/html/jdma_client/tutorial.html#setting-up-the-user-user-settings-and-user-info) section of the JDMA Tutorial.


## UM Rose suite changes

### Rose Edit

1. In panel *suite conf -> JASMIN Elastic Tape*:  
    * Set **Migrate data to JASMIN Elastic Tape** to **True**

2. In panel *postproc -> Post Processing - common settings -> ARCHER2-JASMIN Archiving -> Elastic Tape*:
    * Set **default_workspace** to **False**
    * Enter the JASMIN GWS under which you wish to migrate the data to ET (e.g. ncas_climate).

### Setup connection to JASMIN sci nodes

1. Add the following to your `~/.ssh/config` file on PUMA2:

{% raw %}
~~~
# JASMIN
Host login-0?
User <jasmin-username>
IdentityFile ~/.ssh/<jasmin-ssh-key>
ForwardAgent yes

Host cylc? login-0? sci-vm-0?
Hostname %h.jasmin.ac.uk

Host sci* cylc*
User <jasmin-username>
IdentityFile ~/.ssh/<jasmin-ssh-key>
ForwardAgent yes
ProxyJump login-02
~~~
{% endraw %}

{:start="2"}
2. Add your JASMIN ssh-key to your ssh-agent:

    * `ssh-add ~/.ssh/<jasmin-ssh-key>`

3. Test connection to JASMIN:
   
    *  `ssh sci-vm-03`
    * You should be logged into the JASMIN sci node without prompt for your JASMIN passphrase.

5. Add path to Rose/Cylc to your `~/.bash_profile` on JASMIN:
   
  ~~~
  if [[ $(hostname) = sci*.jasmin.ac.uk || $(hostname) = cylc*.jasmin.ac.uk ]]; then
    # Rose/cylc on jasmin-sci & Lotus nodes
    export PATH=/apps/jasmin/metomi/bin:$PATH
  fi
  ~~~

### Configure PPTransfer
If you haven't already done so follow the instructions for configuring PPTransfer and setting up Globus: [Configuring PPTransfer]({{site.baseurl}}/unified-model/pptransfer)

You may wish to consider using the JASMIN transfer cache disk as the JASMIN transfer destination. This is a large temporary storage area separate to the Group Workspaces. See [JASMIN Transfer Cache](https://help.jasmin.ac.uk/article/4535-xfc) for more information.
