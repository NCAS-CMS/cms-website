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

These instructions assume you have followed the standard PUMA2 setup instructions, 
and that the workflow you are upgrading runs correctly under Cylc 7 on ARCHER2. 

Please also refere to the [Cylc 8 migration guide](https://cylc.github.io/cylc-doc/stable/html/7-to-8/index.html) and the instructions for running [Cylc 8 on PUMA2](/cylc8/).  

## Compatibility mode

Cylc 8 has a [compatibility mode](https://cylc.github.io/cylc-doc/stable/html/7-to-8/major-changes/compatibility-mode.html#cylc-7-compat-mode)
that allows you to run an existing Cylc 7 workflow without fully upgrading. 

On PUMA2-ARCHER2 there are still several changes required, mostly to the top-level runtime settings. 
You may not have to make all these changes to your workflow, but do check all of the points below.
As ever, we can't cover all eventualities so your workflow may required additional changes. 
Get in touch with the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk/) if you need further advice.  

### 1. Check your workflow validates at Cylc 7

Cylc 7 supports some depracted syntax so you will need to upgrade this before moving to Cylc 8. 

Navigate to the `roses` suite directory and run the following: 
```
export CYLC_VERSION=7
rose suite-run --validate 
```

If any warning messages appear, follow the instructions until your suite is fully Cylc 7 compliant.

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

### 2. Remove existing Cylc 7 cylc-run directory

If you are running a workflow that has the same name as a previous Cylc 7 run, you need to either i) rename the current workflow e.g. `u-cz422-cylc8`, or ii) move the old cylc-run directory out of the way first. 

### 3. Check your ssh setup 

It is important that you have the `ssh-setup` script sourced in your `.bash_profile` and not `.bashrc` or any other file. 

**Information**: Cylc 8 job scripts are now launched in a new subshell and this only loads `.bash_profile` by default.
We need to make sure the `ssh-setup` script is run so that any `fcm_make` tasks can mirror code to ARCHER2.

In your `~/.bash_profile` you should have the following: 
```
# Ensure persistent ssh-agent
. $HOME/.ssh/ssh-setup
```

### 4. Add a `remote_setup` task to the graph

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
        [[[job]]]
            execution time limit = PT1M
            batch system = background
~~~
{% endraw %}

### 5. Remove any instances of `[runtime][task][remote]owner`

Cylc 8 no longer supports remote usernames in the workflow definition. 

**Information:** See [here](https://cylc.github.io/cylc-doc/stable/html/7-to-8/major-changes/remote-owner.html) for the details of this change. Remote user names should instead be set in your `.ssh/config` file. 
If you followed the PUMA2 setup instructions, this should already be setup correctly for ARCHER2 and JASMIN. 

Check your `suite.rc` and/or `site/archer2.rc` file and remove any lines like this: 
{% raw %}
~~~
          owner = {{ARCHER2_USERNAME}}
~~~
{% endraw %}

### 6. Update the ARCHER2 slurm flags

The `--export=none` flag should be removed from the ARCHER2 slurm headers. 

**Information:** This setting stops the required run environment from being loaded properly at Cylc 8. If it is included you will see an error like: 
```
/work/n02/n02/annette_test/cylc-run/u-cc519-comp/run1/share/fcm_make/build-recon/bin/um-recon.exe: error while loading shared libraries: libfabric.so.1: cannot open shared object file: No such file or directory
```

Edit your `suite.rc` and/or `site/archer2.rc` and remove the `--export=none` line. It will probably be under `[[HPC]] [[[directives]]]`.

### 7. Set path to Rose/cylc libraries if needed


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

### 8. Make sure fcm make extracts from the mirror repositories

In each of your `fcm_make_*` apps, check that any references to e.g. `fcm:moci.x` are changed to `fcm:moci.xm`.

**Information:** Since Cylc 8 job scripts run under a new subshell, gpg agent will not be available to the fcm make extract tasks, therefore we need to use the MOSRS mirror repositiories on PUMA2. 

### 9. Check your workflow validates at Cylc 8 

Run the following, from the rose workflow directory: 
```
export CYLC_VERSION=8
cylc validate . 
```

If everything is OK you should get the following response: 
```
WARNING - Backward compatibility mode ON
Valid for cylc-8.2.3
```

### 10. Run with Cylc 8 

Run: 
```
cylc vip 
```
