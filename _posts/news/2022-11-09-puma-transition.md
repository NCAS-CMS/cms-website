---
layout: page
subheadline:  "PUMA"
title:  "Transition to new PUMA"
teaser: "Due primarily to the impending retirement of cloud infrastructure within JASMIN we are moving users to a new server called pumanew. Here you will find information on how to log in to the new server and restart any Rose/Cylc suites."
categories:
    - news
tags:
    - news
    - puma
author: ros
#header: no
---


## Login to new PUMA

Please use the address 192.171.169.138 instead of pumatest.nerc.ac.uk in your login line.

## UM workflow ssh-key

Your existing `id_rsa_archerum` key has been copied over from pumatest - **DO NOT** generate a new one.

## How to restart a cylc suite

1. Edit the file `~/cylc-run/SUITEID/log/rose-suite-run.conf` to change `CYLC_VERSION=7.8.7` to `CYLC_VERSION=7.8.12`

2. Ensure the Cylc version in your current environment matches this:
~~~
pumanew$ cylc --version
7.8.12
~~~

3. Restart the suite with `rose suite-restart`.  The suite will continuing running from where it left off on pumatest.

**Note:** If you don't update the cylc version, the suite will continue to run ok, but cylc will fail to pull log files back from the remote machine (e.g. ARCHER2). This is due to a change in the behaviour of the newer version of rsync.

Any problems please raise them on the CMS Helpdesk: [https://cms-helpdesk.ncas.ac.uk/](https://cms-helpdesk.ncas.ac.uk/)

## FAQs

1. How do I access Rose Bush (Cylc Review)?

  Rose Bush (Cylc Review) is currently not available on pumanew due to lack of webserver.

## Known Issues

1. Cylc Graph is currently not working.  We are investigating.


{% comment %} Leave below here {% endcomment %}
## All News Items
{: .t60 }

{% include list-posts tag='news' %}
