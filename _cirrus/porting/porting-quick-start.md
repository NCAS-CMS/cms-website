---
layout: page-fullwidth
title: Quick Start
subheadline: Porting a UM suite to Cirrus
permalink: '/cirrus/porting/quick-start/'
breadcrumb: true
---
The following should be appropriate for most UM vn13.x versions. Unfortunately as UM suites can be configured in multiple ways and there's no "standard" UM job configurations it cannot be guaranteed to work. If there are still issues, please reference the more [detailed instructions]({{ '/cirrus/porting/detailed' | relative_url }}).


### flow.cylc

Search the `flow.cylc` for any reference to **archer2**. If there are none, go onto the next step. Otherwise, change each instance of a reference to `archer2` with `cirrus`.

For example change

`{% raw%}{% set L_REMOTE_SETUP = true if SITE == 'archer2' else false %}{% endraw %}`

to

`{% raw%}{% set L_REMOTE_SETUP = true if SITE == 'cirrus' else false %}{% endraw %}`


### Metadata

In `meta/rose-meta.conf`, locate and change all instances of `archer2` to `cirrus`, `ARCHER2` to `CIRRUS`, `Archer2` to `Cirrus`, etc.

For example:
~~~
[jinja2:suite.rc=ARCHER2_GROUP]
compulsory=true
description=
help=Account code under which to run HPC tasks (e.g. n02-ncas)
ns=host
sort-key=archer2_2
title=Account group for HPC tasks
~~~
should be updated to
~~~
[jinja2:suite.rc=CIRRUS_GROUP]
compulsory=true
description=
help=Account code under which to run HPC tasks (e.g. n02-ncas)
ns=host
sort-key=cirrus_2
title=Account group for HPC tasks
~~~
Also, in `[jinja2:suite.rc=MAIN_ATM_PPN]` or `[jinja2:suite.rc=ATM_PPN]` change `range=1:128` to `range=1:288`

### GUI

Now start up the `rose edit` GUI. There will be a warning triangle next to the **suite conf** section. We need to fix the errors to get rid of the warning triangles.
 * In *suite conf→Host Machine*:
   * Set **Site** to be **Cirrus**
   * Set the **Queue** to **Standard**
   * Set **Account group** by clicking on the plus sign to add it to the configuration, and then set to the required value. \\
   Note: This may be contained in a separate *Project Accounting* panel. Remember to put the account group in single quotes. 

