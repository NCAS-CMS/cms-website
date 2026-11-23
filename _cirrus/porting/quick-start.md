---
layout: page-fullwidth
title: Quick Start
subheadline: Porting a UM suite to Cirrus
permalink: '/cirrus/porting/quick-start/'
breadcrumb: true
---
The following should be appropriate for most UM vn13.x versions. Unfortunately as UM suites can be configured in multiple ways and there's no "standard" UM job configurations it cannot be guaranteed to work. If you have any problems please contact the CMS Helpdesk. 

There are 4 stages in converting an ARCHER suite into a Cirrus suite:

 * Edit the `flow.cylc` file to add Cirrus.
 * Copy the `archer2.rc` or `archer2.cylc` site file to `cirrus.rc` or `cirrus.cylc` and update for Cirrus.
 * Edit the metadata file to add Cirrus options.
 * Update the suite to use Cirrus and change the processor decomposition.


