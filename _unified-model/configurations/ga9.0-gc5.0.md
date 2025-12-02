---
title: GA9.0/GC5.0 Standard Suites
teaser: Information and list of standard suites for the Global Coupled model configuration GC5.0(GC5) and its components (Global Atmosphere and Land 9 (GAL9.0),  Global Ocean and Sea Ice 9 (GOSI9.0)).
---

## Global Atmosphere and Land 9.0

[GA Documentation](https://code.metoffice.gov.uk/trac/gmed/wiki/GADocumentation/GAL9)

### Standard Rose Suites:

| ARCHER2 suite id <br> and revision no. | Owner | Original Met Office <br> suite id | UM Version | Description |
| :------: | :------: | :------: | :------: | :------ | 
| u-co765/archer2 | paulearnshaw | [u-co765](https://code.metoffice.gov.uk/trac/gmed/wiki/Assessment/GADocumentation/GAJobs/u-co765) | 12.2 | GAL9.0 Orca1 N96 12.2 AMIP Climate Assessment (1988 - 2008) (CMIP6 forcing) |


## Global Coupled 5.0

[GC Documentation](https://code.metoffice.gov.uk/trac/gmed/wiki/GCDev/GCDocumentation/GC5)

### Standard Rose Suites:

| ARCHER2 suite id <br> and revision no. | Owner | Original Met Office <br> suite id | UM Version | Description |
| :------: | :------: | :------: | :------: | :------ |
| u-cy010 | rosalynhatcher | [u-cx557](https://code.metoffice.gov.uk/trac/gmed/wiki/GCDev/GCDocumentation/u-cx557)| 13.2 | GC5 N216 ORCA025 UM13.2 YR2000 pesent day control run (cylc7) |
| u-dk922 | dancopsey | [u-dk922](https://code.metoffice.gov.uk/trac/gmed/wiki/GADocumentation/GAJobs/GCDev/GCDocumentation/u-dk922) | 13.9 | GC5 N96-ORCA1 present day control run (Cylc 8) |
| u-da412 | dancopsey | [u-da412](https://code.metoffice.gov.uk/trac/gmed/wiki/GADocumentation/GAJobs/GCDev/GCDocumentation/u-da412) | 13.9 | GC5 N216-ORCA025 present day control run with gregorian calendar (Cylc 8) | 

Users are strongly recommended to use the standard GC5 workflows u-dk922 or u-da412. 
These are updated with each new UM release, and support running on Archer2 and Monsoon3. 

To run on Archer2, take a copy of the base suite, then make the following changes: 
* suite conf &rarr; Machine Options &rarr; site at which model is being run: Change from MetO Cray EX to Archer2
* suite conf &rarr; Account group for HPC tasks: Set to your n02 project code
* suite conf &rarr; Testing &rarr; Test restartability: On &rarr; Off
* postproc &rarr; Post Processing - common settings &rarr; archive_command: Moose &rarr; Archer2-Jasmin

If you wish to use PP Transfer: 
* suite conf &rarr; Build and run &rarr; PP transfer: Off &rarr; On
* postproc &rarr; Archer2-JASMIN Archiving &rarr; Data Transfer -> transfer_dir: Set to your Jasmin space
  
You will also need to make sure you have followed the [Globus setup instructions]({{ 'unified_model/pptransfer-globus' | relative_url }}).

To run ozone redistribution: 
* suite conf &rarr; Ozone Redistribution: false &rarr; true
* suite conf &rarr; Ozone Redistribution &rarr; Host machine for ozone redistribution: MetO Cray EX to Archer2
* suite conf &rarr; Ozone Redistribution &rarr; Primary archive source: Set to be blank

For further details see [ozone redistribution on Archer2]({{ 'unified_model/ozone-redistribution' | relative_url }}). 
