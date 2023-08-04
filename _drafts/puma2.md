---
layout: page-fullwidth
title: PUMA2
teaser: PUMA2
---

***These are draft instructions and are subject to change.***

## PUMA2

We are moving to a new server called PUMA2. 
It will be hosted at ARCHER2, and jointly managed by CMS and EPCC.

Having PUMA2 in the same place as ARCHER2 will make the system easier to navigate, 
and for CMS to manage. 
In particular, you will use the same account to access both machines. 

Upgrading the server also means we will be able to support new UM infrastructure,
such as cylc-8, which will eventually be controlled by a web interface. 
Unfortuantely, the puma server we've been using recently was only an interim solution after the demise of our old machine,
and not suitable as a long-term replacement. 

* [Getting setup](puma2_setup.md)

* [Restarting and running suites](puma2_suites.md)

* [Restarting and running UMUI jobs](puma2_umui.md)


### Summary of changes 

* The ```um``` user account is now ```um1```
* Home directory paths have changed from ```/home/``` to  ```/home/n02/n02/```.
* We have to go via jasmin login2 now.
* The MOSRS password caching scripts are different now. 


### 8. Running suites

You should be able to checkout and run suites as before.

Changes required: 

* In your ```site/archer2.rc``` file replace lines line this:
  ```
  host = login.archer2.ac.uk
  ```
  with this:
  ```
  host = $(rose host-select archer2)
  ```

***This is a placeholder***

### 9. Restarting suites 

***This is a placeholder***

### 10. UMUI 

***This is a placeholder***


