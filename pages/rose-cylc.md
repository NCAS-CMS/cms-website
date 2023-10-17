---
layout: page-fullwidth
title: Rose/Cylc
subheadline: Documentation
teaser: Information on Rose and Cylc, used for running scientific workflows; for example the Unified Model.
permalink: /rose-cylc/
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

## Introduction

Rose is a toolkit for writing, editing and running application configurations.  Rose uses the Cylc workflow engine for running suites of inter-dependent applications. 

## Learning to use Rose/Cylc

### General

* Rose Tutorial: [https://metomi.github.io/rose/doc/html/tutorial/rose/index.html](https://metomi.github.io/rose/doc/html/tutorial/rose/index.html)
* Cylc Tutorial: [https://metomi.github.io/rose/doc/html/tutorial/cylc/index.html](https://metomi.github.io/rose/doc/html/tutorial/cylc/index.html)
* Hints and Tips: [Hints, Tips & Troubleshooting]({{ 'rose-cylc-hints' | relative_url }})
* Rose bush on Monsoon2: `firefox http://localhost/rose-bush`
</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

### Unified Model

* Met Office tutorial on how to run the UM in Rose is available on the Met Office Science Repository Service: [​https://code.metoffice.gov.uk/doc/um/latest/um-training/index.html](​https://code.metoffice.gov.uk/doc/um/latest/um-training/index.html)
* For new users, the [NCAS UM Introduction training course](/services/training/#introduction-to-the-unified-model) gets you started running the UM with Rose. Material from recent courses is always available for reference & self-study.

## Setup

### MOSRS account and password caching 

In order to run UM10.x and newer, access roses-u suite repository or any other codes held in a MOSRS repository you first need an account on the Met Office Science Repository Service (MOSRS). Please contact NCAS-CMS to request an account.

Some setup on Monsoon2 is then required to access the remote repository. This is detailed here:

* [MOSRS FAQ Configuring Subversion Access](https://code.metoffice.gov.uk/trac/home/wiki/FAQ#ConfiguringSubversionaccess) (Note: you need to log in with your MOSRS account to see this)

Then follow the link on "how to cache your password":

* [https://code.metoffice.gov.uk/trac/home/wiki/AuthenticationCaching](https://code.metoffice.gov.uk/trac/home/wiki/AuthenticationCaching)

This is a little complicated so be sure to follow the instructions carefully. 

For ARCHER2 users, the setup is included in the [PUMA2 instruction page]({{ '/puma2/' | relative_url }}). 

### Running on Monsoon2

Rose suites are submitted from the Monsoon2 login nodes.

For Rose Bush run `firefox http://localhost/rose-bush`

A guide to using Rose/Cylc on Monsoon2 can be found in the [Monsoon User Guide](https://code.metoffice.gov.uk/doc/monsoon2/additionalServices.html#rose-and-cylc)

### Running on ARCHER2

Rose suites are submitted from PUMA2.

There is some setup required to enable submission of suites to ARCHER2.  Follow the [PUMA2 setup instructions]({{ '/puma2/' | relative_url }}). 

### Configuring your environment

You can change the default text editors that Rose uses (but note that `gvim` is not available on PUMA):

* [https://metomi.github.io/rose/doc/html/getting-started.html#text-editor](https://metomi.github.io/rose/doc/html/getting-started.html#text-editor)

Syntax highlighting is available for common editors for the Rose and Cylc configuration files. This is really useful if you are editing these by hand (i.e. not through the Rose editor GUI). For instructions see:

* Rose: ​[https://metomi.github.io/rose/doc/html/getting-started.html#editor-syntax-highlighting](https://metomi.github.io/rose/doc/html/getting-started.html#editor-syntax-highlighting)
* Cylc: [https://cylc.github.io/cylc-doc/7.9.3/singlehtml/index.html#syntax-highlighting-for-suite-configuration](https://cylc.github.io/cylc-doc/7.9.3/singlehtml/index.html#syntax-highlighting-for-suite-configuration)

## References

* Cylc User Guide: [https://cylc.github.io/cylc-doc/7.9.3/singlehtml/index.html#document-index](https://cylc.github.io/cylc-doc/7.9.3/singlehtml/index.html#document-index)
* Rose User Guide: [https://metomi.github.io/rose/doc/html/index.html](https://metomi.github.io/rose/doc/html/index.html)
