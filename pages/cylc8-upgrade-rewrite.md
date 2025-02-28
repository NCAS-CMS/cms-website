---

## 4. PUMA2/ARCHER2 specific changes 

### a. Add a `remote_setup` task to the graph

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

### b. Update the ARCHER2 slurm flags

The `--export=none` flag should be removed from the ARCHER2 slurm headers. 

**Information:** This setting stops the required run environment from being loaded properly at Cylc 8. If it is included you will see an error like: 
```
/work/n02/n02/annette_test/cylc-run/u-cc519-comp/run1/share/fcm_make/build-recon/bin/um-recon.exe: error while loading shared libraries: libfabric.so.1: cannot open shared object file: No such file or directory
```

Edit your `suite.rc` and/or `site/archer2.rc` and remove the `--export=none` line. It will probably be under `[[HPC]] [[[directives]]]`.

### c. Make sure FCM extracts from the mirror repositories

In each of your `fcm_make_*` apps, check that any references to e.g. `fcm:moci.x` are changed to `fcm:moci.xm`.

**Information:** Since Cylc 8 job scripts run under a new subshell, gpg agent will not be available to the fcm make extract tasks, therefore we need to use the MOSRS mirror repositiories on PUMA2. 

### d. Set path to Rose/cylc libraries if needed

If you have a script that uses the rose or Cylc python libraries, you will need to set the path directly (since the job environment is no longer inerited). For example the `xml` task for UM-XIOS uses rose macros, so we need: 
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

**Note:** Here we are still using the old version of Rose to run the scripts. To fully upgrade, the scripts would be [updated to Python 3 and the new Rose 2 and Cylc 8 packages](https://cylc.github.io/cylc-doc/latest/html/7-to-8/major-changes/python-2-3.html). 

### e. Change rose date to isodatetime

Instances of `rose date` may need to be  replaced with the [`isodatetime` command](https://cylc.github.io/cylc-doc/stable/html/7-to-8/cheat-sheet.html#datetime-operations). For example, 
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

**Note** The `rose date` command will work on puma2, but it won't work in a task script run on Archer2. So you may not need to change all instances. 

### f. Update cylc variables 

Cylc variables starting with `CYLC_SUITE_` are [now depreacted](https://cylc.github.io/cylc-doc/stable/html/user-guide/writing-workflows/configuration.html#id16) and should be replaced with `CYLC_WORKFLOW_` versions. As of Cylc version 8.4.0 the old variables still work but they may not be equivalent. 

In particular, at Cylc 8 `$CYLC_SUITE_NAME` has the form, `u-de385/run1`.  Replace this with `$CYLC_WORKFLOW_NAME` to get the form `u-de385`. This may be used in pptransfer with `archive_name=$CYLC_SUITE_NAME`. 

### 5. Run with Cylc 8 

