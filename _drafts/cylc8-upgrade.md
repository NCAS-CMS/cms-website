---
layout: page-fullwidth
title: Cylc 8 upgrade
teaser: Instructions for upgrading an ARCHER2 workflow from Cylc 7 to Cylc 8. 
---

These instructions assume you have followed the standard PUMA2 setup instructions, 
and that the workflow you are upgrading runs correctly under Cylc 7 on ARCHER2. 

Please also refere to the Cylc 8 migration guide and the instructions for running Cylc 8 on PUMA2.  

## Compatibility mode

Cylc 8 has a [compatibility mode](https://cylc.github.io/cylc-doc/stable/html/7-to-8/major-changes/compatibility-mode.html#cylc-7-compat-mode)
that allows you to run an existing Cylc 7 workflow without fully upgrading. 

On PUMA2-ARCHER2 there are still several changes required, mostly to the top-level runtime settings. 
You may not have to make all these changes to your workflow, but do check all of the points below.
Your workflow may required additional changes, so do get in touch with the [CMS helpdesk](https://cms-helpdesk.ncas.ac.uk/) if you need further advice.  

### 1. Check your workflow validates at Cylc 7

Cylc 7 supports some depracted syntax, but you will need to upgrade this before moving to Cylc 8. 

Navigate to the `roses` suite directory and run the following: 
```
export CYLC_VERSION=7
rose suite-run --validate 
```

If any warning messages appear, follow the instructions until your suite is fully Cylc 7 compliant.

### 2. Remove existing Cylc 7 cylc-run directory

If you are running a workflow that has the same name as a previous Cylc 7 run, you need to either i) rename the current workflow e.g. `u-cz422-cylc8`, or ii) move the old cylc-run directory out of the way first. 

### 3. Check your ssh setup 

It is important that you have the `ssh-setup` script sourced in your `.bash_profile` and not `.bashrc` or any other file. 
This is because Cylc 8 job scripts are now launched in a new subshell, 
so we need to make sure the ssh agent is available for the `fcm_make` mirroring. 

In your `~/.bash_profile` you should have the following: 
```
# Ensure persistent ssh-agent
. $HOME/.ssh/ssh-setup
```

### 4. Add a `remote_setup` task to the graph

If you have any `fcm_make` tasks in your workflow, the mirror step will try to copy files over to ARCHER2 
before Cylc creates the `cylc-run` directory as a symlink to `$DATADIR`. 
This is because at Cylc 8 [files are not installed until a remote task is actually submitted](https://cylc.github.io/cylc-doc/stable/html/7-to-8/major-changes/cylc-install.html#remote-installation). 

The solution is to have a dummy task that sets up the `cylc-run` directory for the worfklow before the mirrors start.

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

You can no longer specify a remote user name in the workflow definition. 
This should instead be set in your `.ssh/config` file. 
If you followed the PUMA2 setup instructions, this should already be setup correctly for ARCHER2 and JASMIN. 

Check your `suite.rc` and/or `site/archer2.rc` file and remove any lines like this: 
{% raw %}
~~~
          owner = {{ARCHER2_USERNAME}}
~~~
{% endraw %}

### 6. Check the ARCHER2 slurm flags

The `--export=none` flag should be removed from the ARCHER2 slurm headers, 
because it stops the required run environment from being loaded properly at Cylc 8. 
If it is incldued you will see an error like: 
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

Note: We are using the old version of Rose to run the scripts. We will describe how to upgrade to the new Rose 2 and Cylc 8 python packages in the next section. 

### 8. Make sure fcm make extracts from the mirror repositories

Since Cylc 8 job scripts run under a new subshell, gpg agent will not be available to the fcm make extract tasks, therefore we need to use the MOSRS mirror repositiories on PUMA2. 

In each of your `fcm_make_*` apps, check that any references to e.g. `fcm:moci.x` are changed to `fcm:moci.xm`.

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

