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

Please also refer to the [Cylc 8 migration guide](https://cylc.github.io/cylc-doc/stable/html/7-to-8/index.html) and the instructions for running [Cylc 8 on PUMA2](/cylc8/).  

## Overview

This guide lists the steps required to upgrade a workflow from Cylc 7 to Cylc 8 on the PUMA2-ARCHER2 platfom. 
It outlines i) the steps required to update to Cylc 8 syntax and ii) the platform-specific changes required. 
You may not need to make all these changes to your workflow, but do check all of the points listed.

**Information:** Cylc 8 has a [compatibility mode](https://cylc.github.io/cylc-doc/stable/html/7-to-8/major-changes/compatibility-mode.html#cylc-7-compat-mode) that allows you to run an existing Cylc 7 workflow without fully upgrading. 
Given that on PUMA2-ARCHER2 several changes are required even in compatability mode, 
we recommend fully upgrading to Cylc 8.

We can't cover all cases so your workflow may required additional changes. 
Get in touch with the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk/) if you need further advice.

## 1. Check your PUMA2-ARCHER2 setup 

### a. Check your ssh setup 

It is important that you have the `ssh-setup` script sourced in your `.bash_profile` and not `.bashrc` or any other file. 

In your `~/.bash_profile` you should have the following: 
```
# Ensure persistent ssh-agent
. $HOME/.ssh/ssh-setup
```

**Information**: Cylc 8 job scripts are now launched in a new subshell and this only loads `.bash_profile` by default.
We need to make sure the `ssh-setup` script is run so that any `fcm_make` tasks can mirror code to ARCHER2.

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

### b. Check any user-specific settings

Make sure your `.bash_profile` on ARCHER2 has the following line: 
```
. /work/y07/shared/umshared/bin/rose-um-env-puma2
```
Check that this is the **puma2** version and not `rose-um-env-puma`. Also check any other files such as `.profile` or `.bashrc`. 

If you have any user configuration files for Rose or FCM on PUMA2 or ARCHER2, these may cause incompatibilies at Cylc 8. User configurations will be under: `~/.cylc/` and/or `~/.metomi/`. 

## 2. Check your workflow validates at Cylc 7

Cylc 7 supports some depracted syntax so you will need to upgrade this before moving to Cylc 8. 

Navigate to the `roses` suite directory and run the following: 
```
export CYLC_VERSION=7
rose suite-run --validate 
```

Check for any warning messages about deprecated syntax, and follow the instructions until your suite is fully Cylc 7 compliant. These warnings will have the form: 
```
[INFO] 2025-03-17T11:10:21Z WARNING - deprecated items were automatically upgraded in 'suite definition':
[INFO] 2025-03-17T11:10:21Z WARNING -  * (6.4.0) [runtime][postproc_nemo_rst][command scripting] -> [runtime][postproc_nemo_rst][script] - value unchanged
```

## 3. Make Cylc 8 changes 

### a. Update the workflow definition

First rename the `suite.rc` file to`flow.cylc`. 

Then at the top of the `rose suite.conf` file, replace this line: 
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

### b. Update the metadata

Similarly, replace any instances of `jinja2:suite.rc` with `template variables` in the `meta/rose-meta.conf` file.
There may be sub-directories under `meta/` which will also need to be updated. 

### c. Remove any instances of `[runtime][task][remote]owner`

Cylc 8 no longer supports remote usernames in the workflow definition. 

Check your `flow.cylc` and/or `site/archer2.rc` file and remove any lines like this: 
{% raw %}
~~~
          owner = {{ARCHER2_USERNAME}}
~~~
{% endraw %}

**Information:** See [here](https://cylc.github.io/cylc-doc/stable/html/7-to-8/major-changes/remote-owner.html) for the details of this change. Remote user names should instead be set in your `.ssh/config` file. 
If you followed the PUMA2 setup instructions, this should already be setup correctly for ARCHER2 and JASMIN. 

### d. Switch to platforms 

Each task or family that defines a `host` and/or `batch system` should be replaced by a [platform](https://cylc.github.io/cylc-doc/stable/html/reference/config/writing-platform-configs.html#adminguide-platformconfigs). These might be set in the `flow.cylc` file or the `site/archer2.rc` file (or both). 

The platforms should be selected from the [list of supported platform for PUMA2](https://cms.ncas.ac.uk/cylc8/#platforms).
You can also check what platforms are available by running the command `cylc config --platforms`

Some examples: 
<table>
<tr>
<th>Cylc 7</th>
<th>Cylc 8</th>
</tr>
<tr> 
<td><pre>
    [[LINUX]]
        [[[job]]]
            batch system = background
</pre></td>
<td><pre>
    [[LINUX]]
        platform = localhost
</pre></td>
</tr>
<tr></tr>
<tr> 
<td><pre>
    [[HPC]]
        [[[remote]]]
            host = $(rose host-select archer2)
        [[[job]]]
            batch system = slurm
</pre></td>
<td><pre>
    [[HPC]]
        platform = archer2
</pre></td>
</tr>
<tr></tr>
<tr> 
<td><pre>
    [[JASMIN]]
        [[[remote]]]
            host = sci3.jasmin.ac.uk
        [[[job]]]
            batch system = background
</pre></td>
<td><pre>
    [[JASMIN]]
        platform = sci-vm
</pre></td>
</tr>
</table>

**Information:** The [Jasmin updates](https://help.jasmin.ac.uk/docs/software-on-jasmin/rocky9-migration-2024/) mean that most of the old sci nodes have been retired and the sci-vm servers should be used with Cylc 8. 

### e. Update to Cylc 8 syntax 

Then run:
{% raw %}
~~~
export CYLC_VERSION=8
cylc validate .
~~~
{% endraw %}
This produces a list of warnings which describe the remaining syntax changes required to upgrade to Cylc 8. 

For more details refer to the [Cylc 8 migration guide](https://cylc.github.io/cylc-doc/stable/html/7-to-8/summary.html#upgrading-to-cylc-8)

Make changes until `cylc validate .` gives no further warnings. 

## 4. PUMA2-ARCHER2 specific changes 

The workflow should now be updated to Cylc 8, but further changes are required to run properly on ARCHER2. 

### a. Add a `remote_setup` task to the graph

We need a dummy task that sets up the `cylc-run` directory on ARCHER2 before any `fcm_make` mirrors start. 

Edit the `flow.cylc` file, and add in a new task `remote_setup` that runs before any `fcm_make` tasks, e.g.: 
{% raw %}
~~~
{%- if BUILD == true %}
        remote_setup => fcm_make => fcm_make2 => \ 
{%- endif %}
~~~
{% endraw %}

Add the task definition in the appropriate place. 
* i. If your workflow **does not** have a `site/archer2.rc` file, add this to `flow.cylc`: 
{% raw %}
~~~
    [[remote_setup]]
        script = "echo 'Ensure cylc-run set up correctly on remote host.'"
        platform = archer2-bg
        execution time limit = PT1M
~~~
{% endraw %}

* ii. If your workflow **does** have a  `site/archer2.rc` file, add this to the `flow.cylc`: 
{% raw %}
~~~
    [[remote_setup]]
       inherit = None, REMOTE_SETUP_RESOURCE
       script = "echo 'Ensure cylc-run set up correctly on remote host.'"
~~~
{% endraw %}

And this to the `site/archer2.rc`: 
{% raw %}
~~~
    [[REMOTE_SETUP_RESOURCE]]
        platform = archer2-bg
        execution time limit = PT1M
~~~
{% endraw %}

**Information**: On ARCHER2 the cylc-run directory for each workflow is symlinked from `/home` to `/work`. In Cylc 8, the symlink is not set up when the workflow starts, and so the [`fcm_make` mirrror copies data to the wrong location]( https://cylc.discourse.group/t/cylc-8-2-step-fcm-make-and-symlink-dirs/515). 

If you want to run on the nvme filesystem, make sure that you have `platform = archer2-nvme-bg`, as this step is where the link to nvme is created.

### b. Update the ARCHER2 slurm flags

The `--export=none` flag should be removed from the ARCHER2 slurm headers. 

Edit your `flow.cylc` and/or `site/archer2.rc` and remove the `--export=none` line. It will probably be under `[[HPC]] [[[directives]]]`.

**Information:** This setting stops the required run environment from being loaded properly at Cylc 8. If it is included you will see an error like: 
```
/work/n02/n02/annette_test/cylc-run/u-cc519-comp/run1/share/fcm_make/build-recon/bin/um-recon.exe: error while loading shared libraries: libfabric.so.1: cannot open shared object file: No such file or directory
```

### c. Make sure FCM extracts from the mirror repositories

In each of your `fcm_make_*` apps, check that any references to e.g. `fcm:moci.x` are changed to `fcm:moci.xm`.

**Information:** Since Cylc 8 job scripts run under a new subshell, gpg agent will not be available to the fcm make extract tasks, therefore we need to use the MOSRS mirror repositiories on PUMA2. 

### d. Set path to Rose/cylc libraries if needed

If you have a script that uses the rose or Cylc python libraries, you will need to set the path directly (since the job environment is no longer inerited). 

For example the `xml` task for UM-XIOS uses rose macros, so we need: 
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

**Information:** Here we are still using the old version of Rose to run the scripts. To fully upgrade, the scripts would be [updated to Python 3 and the new Rose 2 and Cylc 8 packages](https://cylc.github.io/cylc-doc/latest/html/7-to-8/major-changes/python-2-3.html). 

### e. Change rose date to isodatetime

Instances of `rose date` may need to be replaced with the [`isodatetime` command](https://cylc.github.io/cylc-doc/stable/html/7-to-8/cheat-sheet.html#datetime-operations). For example, 
{% raw %}
~~~
{% set ROSEDATE = "rose date -c --calendar=" + CALENDAR %}
~~~
{% endraw %}
should become: 
{% raw %}
~~~
{% set ROSEDATE = "isodatetime --calendar=" + CALENDAR %}
~~~
{% endraw %}

**Information** The `rose date` command will work on puma2, but it won't work in a task script run on Archer2. 

### f. Update cylc variables 

Cylc variables starting with `CYLC_SUITE_` are [now depreacted](https://cylc.github.io/cylc-doc/stable/html/user-guide/writing-workflows/configuration.html#id16) and should be replaced with `CYLC_WORKFLOW_` versions. As of Cylc version 8.4.0 the old variables still work but they may not be equivalent. 

In particular, at Cylc 8 `$CYLC_SUITE_NAME` has the form, `u-de385/run1`.  Replace this with `$CYLC_WORKFLOW_NAME` to get the form `u-de385`. 

For example, for pptransfer you may have the following set in `app/postproc/rose-app.conf`: 
~~~
archive_name=$CYLC_SUITE_NAME
~~~
Change this to: 
~~~
archive_name=$CYLC_WORKFLOW_NAME
~~~

## 5. Run with Cylc 8 

You should now be able to run your Cylc 8 workflow: 
~~~
export CYLC_VERSION=8
cylc vip
~~~

You can check the progress with the terminal UI: 
~~~
cylc tui <workflow-id>
~~~
