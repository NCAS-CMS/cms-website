---
title: Performance of Standard UM Configurations
teaser: Performance figures for a variety of standard UM configurations on ARCHER2.
---

## Global Atmosphere

| Suite__id | Description | UM Version | Date Run | Decomposition* | Length of run (days) | Dump Frequency (days) | Wallclock (h:m) | Data output vol (GB) | Comment | Cost/model-yr | SYPD | CHSY |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| u-bo026 | GA7 N512 AMIP | 11.4 | 02/21 | A:32x32x2 (26) (80ppn) | 1 | 1 | 00:13 | | | 1800 CU (2.7MAU)| 0.32 | 499,200 |
|         |               |      |       |                      |   |   | 00:25 | | | 3600 CU | |
| u-bs251 | GA7 N96 AMIP | 11.6 | 01/21 | A:16x12x2 (3) | 30 | 30 | 00:30 | 19 | | 18 CU | 4 | |
| u-cd936 | GA7.2.1 N1280 | 11.6 | 05/21 | A:96x64x2 + 2 IOS (96) | 30 | 30 | 07:54 | 524 | Avg over 1 yr run. | 9,424 CU** | 0.25 | 1,206,736 |
 
\* *A = Atmos (EWxNSxOMP) (nodes)* <br>
\** *CU calculation for N1280 includes model failures.* <br>
*Note: SYPD extrapolated from shorter runs.*

## Coupled

| Suite__id | Description | UM Version | Date Run | Decomposition* | Length of run (days) | Dump Frequency (days) | Wallclock (h:m) | Data output vol (GB) | Comment | Cost/model-yr | SYPD | CHSY |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| u-cb151 | GC4 N96 ORCA025 | 11.6 | 01/21 | A:32x20x1 O:32x20x1 X:6 (5:5:1) | 30 | 30 | 01:10 | 43 | | 151 CU | 1.6 | |
| u-cb431 | MetUM-GOML N216 | 10.3 | 09/21 | A:32x24x2 O:64 (12:1) | 30 | 10 | 01:10 | 94 | | 182 CU | 1.67 | |
| u-cn134 | GC3.1 N216 ORCA025 | 11.6 | 02/23 | A:32x32x2 O:32x36x1 X:24 (16:9:6) | 90 | 30 | 03:45 | 126 | |240 CU | | |

\* *A = Atmos (EWxNSxOMP), O = Ocean (EWxNS), X = XIOS processes (nodes)* <br>
*Note: SYPD extrapolated from shorter runs.*

## UKESM

| Suite__id | Description | UM Version | Date Run | Decomposition* | Length of run (days) | Dump Frequency (days) | Wallclock (h:m) | Data output vol (GB) | Comment | Cost/model-yr | SYPD | CHSY |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| u-bz764 | UKESM1 pre-industrial | 11.2 | 12/20 | A:32x18x2 O:12x9 X:8 (9:1:1) | 90 | 90 | 01:41 | 103 | | 73.3 CU (135kAU) | 3.75 | 9349 |
| u-be303 | UKESM AMIP | 11.1 | 12/20 | A:16x16x2 (4) | 90 | 90 | 02:42 | 80 | OOMs on 1 thread | 43.2 CU (82.9kAU) | 2.3 | |
| u-be303 | UKESM AMIP | 11.1 | 12/20 | A:32x18x2 (9) | 90 | 90 | 01:32 | 80 | | 54 CU (103kAU) | 4 | |

\* *A = Atmos (EWxNSxOMP), O = Ocean (EWxNS), X = XIOS processes (nodes)* <br>
*Note: SYPD extrapolated from shorter runs.*



