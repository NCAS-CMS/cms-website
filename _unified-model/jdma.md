---
title: Migration of UM Data to JASMIN Elastic Tape
teaser: Instructions on how to add the JDMA app to a UM Suite to enable migration of model data to JASMIN Elastic Tape as part of the UM Workflow. 
permalink: '/unified-model/jdma'
---

## Setup and initialise JDMA on JASMIN
Before you can use the JDMA to migrate data to Elastic Tape you must install the jdma client on JASMIN and initialise some user settings.
 
1. Install JDMA client software:
    * Login to a JASMIN sci machine
    * Load python2:  
      `module load jaspy/2.7`
    * Create a virtual environment in your home directory:  
      `virtualenv ~/jdma_venv_py2`
    * Activate the virtual environment:  
      `source ~/jdma_venv_py2/bin/activate`
    * Install the jdma client into the virtualenv:  
      `pip install git+https://github.com/cedadev/jdma_client`

2. Follow instructions in the [Setting up the user, user settings and user info](https://cedadev.github.io/jdma_client/docs/build/html/jdma_client/tutorial.html#setting-up-the-user-user-settings-and-user-info) section of the JDMA Tutorial.


## UM Rose suite changes

### Upgrade to postproc_2.4

1. Upgrade fcm_make_pp app:
    * `cd app/fcm_make_pp`
    * `rose app-upgrade -a postproc_2.4`

2. Upgrade postproc app:
    * `cd app/postproc`
    * `rose app-upgrade -M /home/ros/um/um_work/postproc_2.4_archer2_jasmin_rewrite/rose-meta -a pp24_t588`

3. Edit `app/postproc/rose-app.conf`:
    * Set `meta=/home/ros/um/um_work/postproc_2.4_archer2_jasmin_rewrite/rose-meta/archive_and_meaning/postproc/pp24_t588`
 
### Edit Suite Metadata

1. Copy extra metadata to add JDMA switch:
    * `cp -r ~um/metadata/ncas_extras <suite>/meta`

2. Edit the file `<suite>/meta/rose-meta.conf` to add to the top:
    * `import=meta/ncas_extras`

### Rose Edit

1. In panel *suite conf -> JASMIN Elastic Tape*:  
    * Set **Migrate data to JASMIN Elastic Tape** to **True**

2. In panel *fcm_make_pp -> configuration* set:
    * **config_base:** fcm:moci.xm-br/dev/rosalynhatcher/postproc_2.4_archer2_jasmin_rewrite
    * **config_rev:** <blank>
    * **pp_rev:** postproc_2.4
    * **pp_sources:** branches/dev/rosalynhatcher/postproc_2.4_archer2_jasmin_rewrite@4462

3. In panel *postproc -> Post Processing - common settings -> ARCHER2-JASMIN Archiving -> Elastic Tape*:
    * Set **default_workspace** to **False**
    * Enter the JASMIN GWS under which you wish to migrate the data to ET (e.g. ncas_climate).

### Add Tasks to suite.rc File

As suites vary in their structure it is impossible to provide instructions that will cover all eventualities.  The following points are provided for guidance only.  We need to add the build of postproc jdma scripts and the `jdma` task to the suite graph so that it runs after the `pptransfer` task has run.

1. Add `fcm_make_pp_jamsin` tasks to cylc graph in `[[[R1]]]`. After the line:
``` 
 {{ 'fcm_make_pp => fcm_make2_pp' + (' => POSTPROC_GROUP' if RUN else '')}}
``` 
insert
``` 
 {{ 'fcm_make_pp_jasmin => fcm_make2_pp_jasmin => jdma' if JDMA else '' }}
```
 
{:start="2"}
2. Locate `pptransfer` in the cylc graph. For UKESM and GA suites this is something like:
```{% raw %}
    graph =
    ...
    {% if PPTRANSFER %}
pptransfer {{'=> \\' if HOUSEKEEP else '' }}
    {% endif %}
    ...
{% endraw %} ```

  Change this to be:

```{% raw %}
     graph =
    ...
    {% if PPTRANSFER %}
pptransfer {{'=> \\' if JDMA or HOUSEKEEP else '' }}
    {% endif %}
    {% if JDMA %}
jdma {{'=> \\' if HOUSEKEEP else '' }}
    {% endif %}
    ...
{% endraw %} ```
 
{:start="3"}
3. Add jdma task definition to end of file before any {% raw %} {% include ... %} {% endraw %}:
```{% raw %}
 {% if JDMA %}
    [[JASMIN]]
        [[[environment]]]
            PLATFORM = Linux
            UMDIR = ~um
            OCEANDIR = ~um
        [[[remote]]]
            host = sci5.jasmin.ac.uk
        [[[job]]]
            batch system = background

    [[PPBUILD_RESOURCE_JASMIN]]
        inherit = JASMIN
        [[[job]]]
            execution time limit = PT20M

    [[fcm_make_pp_jasmin]]
        inherit = None, EXTRACT_RESOURCE
        [[[environment]]]
            ROSE_TASK_APP = fcm_make_pp

    [[fcm_make2_pp_jasmin]]
        inherit = None, PPBUILD_RESOURCE_JASMIN
        [[[environment]]]
            ROSE_TASK_APP = fcm_make_pp

    [[JDMA_RESOURCE]]
        inherit = JASMIN
        pre-script = "PS1=${PS1:-}; source /home/users/rshatcher/venvs/jdma_venv_py2/bin/activate"
        [[[job]]]
            execution time limit = PT1H

    [[jdma]]
        inherit = JDMA_RESOURCE
        [[[environment]]]
            CYCLEPERIOD = {{FMT}}
            ROSE_TASK_APP = postproc
{% endif %}
{% endraw %}```

### Setup connection to JASMIN sci nodes

1. Add the following to your `~/.ssh/config` file on PUMA:
{% raw %}
~~~
# JASMIN
Host login1
Hostname login1.jasmin.ac.uk
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
ProxyCommand ssh -Y login1 -W %h:%p
ControlMaster auto
ControlPath /tmp/ssh-socket-%r@%h-%p
ControlPersist yes
~~~
{% endraw %}

{:start="2"}
2. Add your JASMIN ssh-key to your ssh-agent:
    * `ssh-add ~/.ssh/<jasmin-ssh-key>`

3. Test connection to JASMIN:
    *  `ssh sci3.jasmin.ac.uk`
    * You should be logged into the JASMIN sci node without prompt for your JASMIN passphrase.

4. Add path to Rose/Cylc to your `~/.bash_profile` on JASMIN:
~~~
if [[ $(hostname) = sci*.jasmin.ac.uk || $(hostname) = cylc*.jasmin.ac.uk ]]; then
  # Rose/cylc on jasmin-sci & Lotus nodes
  export PATH=/apps/jasmin/metomi/bin:$PATH
fi
~~~

### Configure PPTransfer
If you haven't already done so follow the instructions for configuring PPTransfer and setting up Gridftp certificate: [Configuring PPTransfer]({{site.baseurl}}/unified-model/pptransfer)

You may wish to consider using the JASMIN transfer cache disk as the JASMIN transfer destination. This is a large temporary storage area separate to the Group Workspaces. See [JASMIN Transfer Cache](https://help.jasmin.ac.uk/article/4535-xfc) for more information.
