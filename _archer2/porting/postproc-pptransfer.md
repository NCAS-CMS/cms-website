---
layout: page-fullwidth
title: Post-processing
subheadline: Porting a UM suite to ARCHER2
permalink: '/archer2/porting/postproc-pptransfer/'
breadcrumb: true
---
In `~/roses/<SUITEID>/site/archer2.rc` ensure that `[[POSTPROC_RESOURCE]]` loads the correct module and sets the stack limit, thus:
~~~
    [[POSTPROC_RESOURCE]]
        inherit = HPC_SERIAL
        pre-script = """module load postproc
                        module list 2>&1
                        ulimit -s unlimited
                     """
~~~
For **coupled jobs** make the following suite changes:

* Ensure the suite is using **postproc_2.3**.
* In *fcm_make_pp → Configuration*:
  * Set **config_base** to `fcm:moci.xm-br/dev/annetteosprey/postproc_2.3_archer2`
  * Remove contents of **config_rev** so it is blank.
  * In **pp_sources** ensure the following 2 branches are listed: \\
  `fcm:moci.xm-br/dev/annetteosprey/postproc_2.3_archer2@3910` \\
  `fcm:moci.xm-br/dev/rosalynhatcher/postproc_2.3_pptransfer_gridftp_nopw@3202`
* In postproc → CICE → Diagnostics → Meaning
  * Set **means_cmd** to `ncra --64bit_offset -O`
  * **Note:** Some suites have an optional configuration override file so you may find you need to change this in the override file: `app/postproc/opt/rose-app-archer2.conf`

For guidance on configuring the data transfer app see: [Configuring PPTransfer]({{ '/archer2/pptransfer' | relative_url }}).
