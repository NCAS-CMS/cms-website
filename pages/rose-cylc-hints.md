---
layout: page-fullwidth
title: Rose/Cylc Hints, Tips & Troubleshooting
subheadline: Documentation
teaser: Useful information for running with Rose/Cylc
permalink: /rose-cylc-hints/
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

## Hints & Tips
### Switching versions of Rose and/or Cylc

Set the following variables to use a different version of Rose and/or Cylc to the default:
~~~
  export CYLC_VERSION=x.y.z
  export ROSE_VERSION=YYYY.MM.VV
~~~
e.g.
~~~
  export CYLC_VERSION=7.8.6
  export ROSE_VERSION=2021.01.01
~~~
Note: you should use the same versions of Rose and Cylc on both PUMA and ARCHER2.

### Switching versions of Rose/cylc for a running suite

First you need to stop the suite via the GUI or with: `cylc stop --name=SUITE`, where `SUITE` is the suite name. If the cylc version in your enviornment is different to the one the suite is using you may need to set the cylc version prior to running the command `CYLC_VERSION=x.y.z cylc stop SUITE`.

Wait for the suite to complete cleanly:

* Look at the end of `~/cylc-run/SUITE/log/suite/log`, which should tell you the suite is shutting down with a reason.
* Look at the end of `~/cylc-run/SUITE/log/suite/out`, which should say `DONE`. 

Modify the `CYLC_VERSION` and `ROSE_VERSION` variables in `~/cylc-run/SUITE/log/rose-suite-run.conf`.

Ensure the Cylc and Rose versions in your current environment match the version you are trying to use. Run `rose --version` and `cylc --version`).

Then restart the suite with: `rose suite-restart --name=SUITE`. (Note you should NOT run `rose suite-run --restart`).

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

### Viewing the suite run graph without running

When developing suites, it can be useful to check what the run graph looks like after jinja evaluation etc. To do this without running the suite:
~~~
rose suite-run -i --name=puma-aa045  # install suite in cylc db only
cylc graph puma-aa045                # view graph in browser       
~~~
To just view the dependencies on the command line:
~~~
cylc ls -t puma-aa045
~~~

### Setting the default size of the rose edit window

Setting the default size of the `rose edit` window and the width of the `rose edit` left hand menu pane can be very helpful.

Edit `~/.metomi/rose.conf`

Adding the following information to the file sets the default size and width of the `rose config-edit` (`rose edit`) window:
~~~
[rose-config-edit]
SIZE_WINDOW = (1100, 650)
WIDTH_TREE_PANEL = 400
~~~
For details of further customisations that can be made to the rose edit window see: ​[https://metomi.github.io/rose/doc/html/api/configuration/site-and-user.html#site-and-user-configuration ](https://metomi.github.io/rose/doc/html/api/configuration/site-and-user.html#site-and-user-configuration)

### Launching Rose commands

It is possible to launch many of the Rose tools from the various GUIs. For example you can run or edit suites from `rosie go`, run suites from `rose edit`, and view log files from `rose suite-gcontrol` whilst the suite is running.

When running rose from the command line make sure to run from the appropriate roses/ directory or append the suite name using `--name=u-aa015`, e.g.
~~~
rose suite-shutdown --name=u-aa015
~~~

Be careful though because `rose suite-run --name=u-aa0015` works differently. It would run the suite in the current directory but re-name it `u-aa015`.

### Stop archiving of log files

By default, when a suite is run, the log files from the previous run will be tarred up. To avoid this run `rose suite-run` with the flag `--no-log-archive`.

### Diff'ing suites

There is no formal mechanism for this. But there is a tool `rose config-dump` which sort all of the app files in the suite into a common format, which then allows for diff to be run on the command-line between suite files. For more info see: ​[https://metomi.github.io/rose/doc/html/api/command-reference.html#rose-config-dump](https://metomi.github.io/rose/doc/html/api/command-reference.html#rose-config-dump)

### Adding UM user diagnostics

This works in a different way to the old UMUI and no longer uses user-STASHmaster files.

Instead the STASHmaster file is held in the UM trunk. To make changes, place your modified version in the `file/` subdirectory of the app, e.g:
~~~
~roses/u-aa045/app/um/file/STASHmaster
~~~

### Passing arguments to fcm_make

Rose deals with `fcm_make` as a special app, see: ​[https://metomi.github.io/rose/doc/html/api/built-in/fcm_make.html](https://metomi.github.io/rose/doc/html/api/built-in/fcm_make.html)

To pass arguments, such as `-vvv` for full verbose output:

* Set the environment variable `ROSE_TASK_OPTIONS=-vvv`
* Or add `args=-vvv` at the top of the `fcm_make` `rose-app.conf` file.

### Merging in changes from another suite

You may have taken a copy of a suite, but there have been subsequent changes that you wish to include. FCM won't allow you to merge in changes from another suite, but you can do it with a direct svn command. You will need to know the full svn URL for the suite containing the changes and the revision number (use -c) or range (use -r), for example:
~~~
svn merge -c 23406 https://code.metoffice.gov.uk/svn/roses-u/a/a/7/7/4/trunk
svn merge -r 21186:23406  https://code.metoffice.gov.uk/svn/roses-u/a/a/7/7/4/trunk
~~~

If there are any clashes, you will need to resolve them.

### Check which suites you have running

For a command-line listing of your running suite:
~~~
rose suite-scan 
~~~
To see a graphical summary status of all of your suites, use:
~~~
cylc gscan & 
~~~
You can then click on each of the suites to open the usual cylc suite control GUI.

## Troubleshooting Common Errors

### No gcylc window

When submitting a job, no `gcylc` window appears.

Sometimes the gui is slow to load. If it does not appear at all however, check that you have X11 forwarding set up from your initial location and the lander.

To do so `ssh` with the `-Y` option or alternatively, append the following line to your `~/.ssh/config` file:
~~~
Host *
ForwardX11 yes
~~~

### Problems shutting down suites

See our UM training material on [how to shutdown stuck suites](https://ncas-cms.github.io/um-training/useful-information.html#problems-shutting-down-suites)

### Jinja error from rose suite-run

After editing the suite, a cryptic Jinja error message appears from rose suite-run:
~~~
[FAIL] cylc validate -v --strict u-aa069 # return-code=1, stderr=
[FAIL] Jinja2 Error:
[FAIL]   File "<unknown>", line 58, in template
[FAIL] TemplateSyntaxError: expected token 'end of print statement', got '='
~~~
This is caused by some error in the `suite.rc` file caused by the Jinja syntax or Rose variables.

To debug, go to `~/cylc-run/<suite-name>`, open the `suite.rc` file and navigate to the line number causing the error.

If the `suite.rc` file uses includes, then to generate the parsed file run:
~~~
cylc view -i <suite-name>
~~~
After identifying the error, fix in the original `suite.rc` or `rose-suite.conf` file in the roses directory. Editing the file in the `cylc-run` directory will have no effect!

### Can't view output in Rose Bush

Sometimes clicking on the log file in Rose bush gives a "403 Forbidden" error with a Python traceback:
~~~
Traceback (most recent call last):
  File "/usr/local/python/lib/python2.6/site-packages/cherrypy/_cprequest.py", line 606, in respond
    cherrypy.response.body = self.handler()
  File "/usr/local/python/lib/python2.6/site-packages/cherrypy/_cpdispatch.py", line 25, in __call__
    return self.callable(*self.args, **self.kwargs)
  File "/home/fcm/rose/lib/python/rose/bush.py", line 301, in view
    f_name = self._get_user_suite_dir(user, suite, path)
  File "/home/fcm/rose/lib/python/rose/bush.py", line 472, in _get_user_suite_dir
    *paths))
  File "/home/fcm/rose/lib/python/rose/bush.py", line 446, in _check_dir_access
    raise cherrypy.HTTPError(403)
HTTPError: (403, None)
~~~
This is because the Rose bush server does not have permissions to read the log file. Navigate to your log files on the command line then manually add read permissions:
~~~
cd ~/cylc-run/<suite-id>/log
chmod -R a+r *
~~~
Then refresh the browser and the file should appear.

So that future log files have the correct permission add the line `-W umask = 0022` to your `suite.rc` under the [[HPC]] [`[[directives][]]` namespace:
~~~
    [[XC30]]
...
        [[[directives]]]
...
            -W umask = 0022
~~~
Sometimes log files may also not show up if connection has been lost between PUMA and ARCHER2. In this case log on to ARCHER2, and navigate to the suite output directory:
~~~
chmod -R a+r ~/cylc-run/<suite-id>/log/job
~~~
Then browse the log files manually. You should also check your ssh agent on PUMA is still active.

### Unable to access STASHmaster from branch on ARCHER2

Some suites may reference files held in the repository for use at runtime. The most common example of this is the STASHmaster file. To make a change to the STASHmaster file requires editing the file in a branch and setting the path to this in the suite. However the method described in the instructions below will not work on ARCHER2:

​[https://code.metoffice.gov.uk/doc/um/latest/um-training/stashmaster.html](https://code.metoffice.gov.uk/doc/um/latest/um-training/stashmaster.html)

You will get an error like:
~~~
[FAIL] file:STASHmaster=source=fcm:um.xm_tr/rose-meta/um-atmos/HEAD/etc/stash/STASHmaster@31236: bad or missing value
Received signal ERR
~~~
This is because the job tries to access the repository from the ARCHER2 queues, which will not work. Note this will work on the XCS machines, so if you are porting a suite, it may have something like this in.

The solution is to make the suite extract the file on PUMA and then copy over to ARCHER2 with the other suite files.

You will have a line in `app/um/rose-app.conf` such as:
~~~
[file:STASHmaster]
source=fcm:um.xm_tr/rose-meta/um-atmos/HEAD/etc/stash/STASHmaster@31236
~~~
This should be removed, and the following added to the rose-suite.conf file:
~~~
[file:app/um/file/STASHmaster] 
source=fcm:um.xm_tr/rose-meta/um-atmos/HEAD/etc/stash/STASHmaster@31236
~~~
Note the `source=` line is identical but the target `[file:]` line needs to reflect the intended location in the suite directory structure.

This will extract the file on PUMA and install it to the app/um directory on ARCHER2 which will have exactly the same affect as extracting on ARCHER2 directly would have done.

This method will work for any similar files. 