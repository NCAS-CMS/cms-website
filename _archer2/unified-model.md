---
layout: page-fullwidth
title: Unified Model on ARCHER2
subheadline: ARCHER2
teaser: CMS have installed UM versions 7.3, 8.4, 10.7, 11.1+, 12.x & 13.x on ARCHER2
permalink: '/archer2/unified-model/'
breadcrumb: true
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

## Getting Started

Several setup steps are required before running the UM for the first time on ARCHER2:

For those that have never run the UM before:
* Register for an [ARCHER2 account](https://docs.archer2.ac.uk/quick-start/quickstart-users/#request-an-account-on-archer).
* Register for a PUMA account by contacting the [CMS Team]({{ '/contact/' | relative_url}}).
* Setup your PUMA and ARCHER2 environments by following the [set up instructions](https://ncas-cms.github.io/um-training/getting-setup.html#set-up-your-archer2-environment) in our online training.

For those that have previously run the UM on ARCHER:
* Register for an [ARCHER2 account](https://docs.archer2.ac.uk/quick-start/quickstart-users/#request-an-account-on-archer).
* Setup your ARCHER2 environment. Ensure you have the following line in your `~/.bash_profile` on ARCHER2: \\
  `. /work/y07/shared/umshared/bin/rose-um-env` \\
  **Note:** the path change from ARCHER.

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

## UMDIR (umshared)

All UM data and software is installed centrally under `/work/y07/shared/umshared`.

UKCA input files that used to be under `/work/n02/n02/ukca` on ARCHER now reside under `/work/y07/shared/umshared/ukca`.

Users may set `UMDIR` in their `~/.bash_profile` but remember that batch jobs can't see `/home` and therefore will not source any scripts that reside there.

## Standard Suites

CMS maintain a number of standard suite configuations on ARCHER2. All standard suites available are detailed on the [UM Configurations]({{ '/unified-model/configurations' | relative_url }}) page.

## Performance

The performance of various standard configurations on ARCHER can be found on the [performance](/unified-model/performance/) page.
