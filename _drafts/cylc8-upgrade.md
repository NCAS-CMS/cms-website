---
layout: page-fullwidth
title: Cylc 8 upgrade
teaser: Instructions for upgrading an ARCHER2 workflow from Cylc 7 to Cylc 8. 
---

These instructions assume you have followed the standard PUMA2 setup instructions, 
and that the workflow you are upgrading runs correctly under Cylc 7 on ARCHER2. 

## Compatibility mode

Cylc 8 has a [compatibility mode](https://cylc.github.io/cylc-doc/stable/html/7-to-8/major-changes/compatibility-mode.html#cylc-7-compat-mode)
that allows you to run an existing Cylc 7 workflow without fully upgrading. 

On PUMA2-ARCHER2 there are still several changes required. 

### 1. Check your workflow validates at Cylc 7

Cylc 7 supports some depracted syntax, but you will need to upgrade this before moving to Cylc 8. 

Navigate to the `roses` suite directory and run the following: 
```
export CYLC_VERSION=7
rose suite-run --validate 
```

If any warning messages appear, follow the instructions until your suite is fully Cylc 7 compliant.

### 2. Check your ssh setup 

It is important that you have the `ssh-setup` script sourced in your `.bash_profile` and not `.bashrc` or any other file. 
This is because Cylc 8 job scripts are now launched in a new subshell, 
so we need to make sure the ssh agent is available for the `fcm_make` mirroring. 

In your `~/.bash_profile` you should have the following: 
```
# Ensure persistent ssh-agent
. $HOME/.ssh/ssh-setup
```

### 3. Add a `remote_setup` task to the graph

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

### 4. Remove any instances of `[runtime][task][remote]owner`

You can no longer specify a remote user name in the workflow definition. 
This should instead be set in your `.ssh/config` file. 
If you followed the PUMA2 setup instructions, this should already be setup correctly for ARCHER2 and JASMIN. 

Check your `suite.rc` and/or `site/archer2.rc` file and remove any lines like this: 
{% raw %}
~~~
          owner = {{ARCHER2_USERNAME}}
~~~
{% endraw %}

### 5. Check the ARCHER2 slurm flags

The line `--export=none` should be removed from ARCHER2 slurm headers, 
because it stops the required run environment from being loaded properly at Cylc 8. 

Edit your `suite.rc` and/or `site/archer2.rc` file to remove the line, which will probably be under `[[HPC]] [[[directives]]]`.

### 6. Set path to Rose/cylc libraries

If you have a script that uses the rose or cylc python libraries, you will need to set the path directly (since the job environment is no longer inerited). For example the `xml` task for UM-XIOS uses rose macros. You can set the Python path using the [`ROSE_PYTHONPTH`](
https://cylc.discourse.group/t/rose-pythonpath/862) environment variable, e.g.: 
{% raw %}
~~~
    [[XML_RESOURCE]]
        inherit = HPC_SERIAL
	pre-script = """
                     export ROSE_PYTHONPATH=/work/y07/shared/umshared/metomi/cylc-7/lib/python:$PYTHONPATH
                     """
~~~
{% endraw %}

To upgrade your scripts to Python 3 and the new Cylc 8 and Rose 2 libraries, see the next section. 
