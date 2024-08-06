---
layout: page-fullwidth
title: Upgrading to Cylc 8
teaser: Instructions for upgrading an ARCHER2 workflow from Cylc 7 to Cylc 8. 
permalink: /cylc8/upgrading-workflows/
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

***We are still in the process of testing Cylc 8 on PUMA2 and ARCHER2. These instructions are under development.*** 

These instructions assume you have followed the standard PUMA2 setup instructions, 
and that the workflow you are upgrading runs correctly under Cylc 7 on ARCHER2. 

Please also refer to the [Cylc 8 migration guide](https://cylc.github.io/cylc-doc/stable/html/7-to-8/index.html) and the instructions for running [Cylc 8 on PUMA2](/cylc8/).  

# Overview

Cylc 8 has a [compatibility mode](https://cylc.github.io/cylc-doc/stable/html/7-to-8/major-changes/compatibility-mode.html#cylc-7-compat-mode)
that allows you to run an existing Cylc 7 workflow without fully upgrading. 

**Important: On PUMA2-ARCHER2 there are still several changes required to run even in compatability mode.** 

These are mostly just changes to the top-level runtime settings. 
You may not have to make all these changes to your workflow, but do check all of the points below.
As ever, we can't cover all eventualities so your workflow may required additional changes. 
Get in touch with the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk/) if you need further advice.

After making these changes, you should then fully upgrade to Cylc 8. This is mainly syntax change to the suite definition files, 
including replacing remote "hosts" with "[platforms](https://cylc.github.io/cylc-doc/stable/html/reference/config/writing-platform-configs.html#adminguide-platformconfigs)". 


# 1. Check your PUMA2/ARCHER2 setup 

## a. Check your ssh setup 

It is important that you have the `ssh-setup` script sourced in your `.bash_profile` and not `.bashrc` or any other file. 

**Information**: Cylc 8 job scripts are now launched in a new subshell and this only loads `.bash_profile` by default.
We need to make sure the `ssh-setup` script is run so that any `fcm_make` tasks can mirror code to ARCHER2.

In your `~/.bash_profile` you should have the following: 
```
# Ensure persistent ssh-agent
. $HOME/.ssh/ssh-setup
```

## b. Check any user-specific settings

Make sure your `.bash_profile` on ARCHER2 has the following line: 
```
. /work/y07/shared/umshared/bin/rose-um-env-puma2
```
Check that this is the **puma2** version and not `rose-um-env-puma`. Also check any other files such as `.profile` or `.bashrc`. 

If you have any user configuration files for Rose or FCM on PUMA2 or ARCHER2, these may cause incompatibilies at Cylc 8. Rose and FCM configurations are under `.metomi`. 

## c. Remove potentially conflicting Cylc 7 cylc-run directories

If you are running a workflow that has the same name as a previous Cylc 7 run, you need to either i) rename the current workflow e.g. `u-cz422-cylc8`, or ii) move the old cylc-run directory out of the way first. Make sure there are no conflicting cylc-run directories on either puma2 or archer2. 

# 2. Check your workflow validates at Cylc 7

Cylc 7 supports some depracted syntax so you will need to upgrade this before moving to Cylc 8. 

Navigate to the `roses` suite directory and run the following: 
```
export CYLC_VERSION=7
rose suite-run --validate 
```

If any warning messages appear, follow the instructions until your suite is fully Cylc 7 compliant.

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

# 3. Make Cylc 8 compatibility changes to your suite

## a. Add a `remote_setup` task to the graph

We need a dummy task that sets up the `cylc-run` directory on ARCHER2 before any `fcm_make` mirrors start. 

**Information**: On ARCHER2 the cylc-run directory for each workflow is symlinked from `/home` to `/work`. In Cylc 8, the symlink is not set up when the workflow starts, and so the [`fcm_make` mirrror copies data to the wrong location]( https://cylc.discourse.group/t/cylc-8-2-step-fcm-make-and-symlink-dirs/515). 

Edit the `suite.rc` file, and add in a new task `remote_setup` that runs before any `fcm_make` tasks, e.g.: 
{% raw %}
~~~
{%- if BUILD == true %}
        remote_setup => fcm_make => fcm_make2 => \ 
{%- endif %}
~~~
{% endraw %}

Add the task definition in the appropriate place. 
* i. If your workflow **does not** have a `site/archer2.rc` file, add this to `suite.rc`: 
{% raw %}
~~~
    [[remote_setup]]
        inherit = HPC
        script = "echo 'Ensure suite dir set up correctly on remote host.'"
        [[[job]]]
            execution time limit = PT1M
            batch system = background
~~~
{% endraw %}

* ii. If your workflow **does** have a  `site/archer2.rc` file, add this to the `suite.rc`: 
{% raw %}
~~~
    [[remote_setup]]
       inherit = None, REMOTE_SETUP_RESOURCE
       script = "echo 'Ensure suite dir set up correctly on remote host.'"
~~~
{% endraw %}

And this to the `site/archer2.rc`: 
{% raw %}
~~~
    [[REMOTE_SETUP_RESOURCE]]
        inherit = HPC
        [[[job]]]
            execution time limit = PT1M
            batch system = background
~~~
{% endraw %}

## b. Remove any instances of `[runtime][task][remote]owner`

Cylc 8 no longer supports remote usernames in the workflow definition. 

**Information:** See [here](https://cylc.github.io/cylc-doc/stable/html/7-to-8/major-changes/remote-owner.html) for the details of this change. Remote user names should instead be set in your `.ssh/config` file. 
If you followed the PUMA2 setup instructions, this should already be setup correctly for ARCHER2 and JASMIN. 

Check your `suite.rc` and/or `site/archer2.rc` file and remove any lines like this: 
{% raw %}
~~~
          owner = {{ARCHER2_USERNAME}}
~~~
{% endraw %}

## c. Update the ARCHER2 slurm flags

The `--export=none` flag should be removed from the ARCHER2 slurm headers. 

**Information:** This setting stops the required run environment from being loaded properly at Cylc 8. If it is included you will see an error like: 
```
/work/n02/n02/annette_test/cylc-run/u-cc519-comp/run1/share/fcm_make/build-recon/bin/um-recon.exe: error while loading shared libraries: libfabric.so.1: cannot open shared object file: No such file or directory
```

Edit your `suite.rc` and/or `site/archer2.rc` and remove the `--export=none` line. It will probably be under `[[HPC]] [[[directives]]]`.

## d. Set path to Rose/cylc libraries if needed

If you have a script that uses the rose or cylc python libraries, you will need to set the path directly (since the job environment is no longer inerited). For example the `xml` task for UM-XIOS uses rose macros, so we need: 
{% raw %}
~~~
    [[XML_RESOURCE]]
        inherit = HPC_SERIAL
	pre-script = """
                     export PATH=/work/y07/shared/umshared/metomi/rose-2019.01/bin:$PATH
                     export PYTHONPATH=/work/y07/shared/umshared/metomi/rose-2019.01/lib/python:$PYTHONPATH
                     """
~~~
{% endraw %}

**Note:** Here we are still using the old version of Rose to run the scripts. We will describe how to upgrade to the new Rose 2 and Cylc 8 python packages in the next section. 

## e. Make sure fcm make extracts from the mirror repositories

In each of your `fcm_make_*` apps, check that any references to e.g. `fcm:moci.x` are changed to `fcm:moci.xm`.

**Information:** Since Cylc 8 job scripts run under a new subshell, gpg agent will not be available to the fcm make extract tasks, therefore we need to use the MOSRS mirror repositiories on PUMA2. 

# 4. Check Cylc 7 compatibility mode

## a. Check your workflow validates at Cylc 8 

Run the following, from the rose workflow directory: 
```
export CYLC_VERSION=8
cylc validate . 
```

If everything is OK you should get the following response: 
```
WARNING - Backward compatibility mode ON
Valid for cylc-8.3.2
```

## b. (Optionally) run in cylc 8 with compatibility mode 

You should be able to run your suite under Cylc 8 at this point.  
```
cylc vip 
```
Note that this is still using old Cylc 7 syntax and you will need to fully upgrade to Cylc 8. 

# 5. Uprade to a Cylc 8 workflow 

## a. Add in workflow definition

First rename the `suite.rc` file to`flow.cylc`. 

Then at the top of the `rose suite.conf` file, replace the line: 
{% raw %}
~~~
[jinja2:suite.rc]
~~~
{% endraw %}
with 
{% raw %}
~~~
[template variables]
~~~
{% endraw %}

## b. Switch to platforms 

Each task or family that defines a `host` and/or `batch system` should be replaced by a [platform](https://cylc.github.io/cylc-doc/stable/html/reference/config/writing-platform-configs.html#adminguide-platformconfigs). These might be set in the `suite.rc` file or the `site/archer2.rc` file (or both). For example: 

* i. localhost
{% raw %}
~~~
    [[NCAS_NOT_SUPPORTED]]
        [[[job]]]
            batch system = background
~~~
{% endraw %}
becomes
{% raw %}
~~~
    [[NCAS_NOT_SUPPORTED]]
        platform = localhost
~~~
{% endraw %}

* ii. ARCHER2 slurm 
{% raw %}
~~~
    [[HPC]]
        [[[remote]]]
            host = $(rose host-select archer2)
        [[[job]]]
            batch system = slurm 
~~~
{% endraw %}
becomes
{% raw %}
~~~
    [[HPC]]
        platform = archer2
~~~
{% endraw %}

* iii Jasmin sci node background
{% raw %}
~~~
    [[JASMIN]]
        [[[remote]]]
            host = sci2.jasmin.ac.uk
        [[[job]]]
            batch system = background
~~~
{% endraw %}
becomes
{% raw %}
~~~
    [[JASMIN]]
        platform = sci_bg
~~~
{% endraw %}

The platforms should be selected from the [list of supported platform for PUMA2](https://cms.ncas.ac.uk/cylc8/#platforms). 

## c. Update to Cylc 8 syntax 

Then run:
{% raw %}
~~~
cylc validate .
~~~
{% endraw %}
This produces a list of warnings which describe the syntax changes required to upgrade to Cylc 8. 

For more details refer to the https://cylc.github.io/cylc-doc/stable/html/7-to-8/summary.html#upgrading-to-cylc-8

## d. Run with Cylc 8

Once you can run `cylc validate .` with no warnings, you are ready to try running your suite at Cylc 8 with: 
{% raw %}
~~~
cylc vip
~~~
{% endraw %}
