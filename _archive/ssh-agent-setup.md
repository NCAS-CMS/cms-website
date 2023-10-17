---
layout: page-fullwidth
title: SSH setup for submission of UM suites
subheadline: ARCHER2
#permalink: '/archer2/ssh-agent-setup/'
breadcrumb: true
---

In order to be able to submit UM suites from PUMA to ARCHER2 you must have ssh access setup correctly.  

{% include alert important='Important: You DO NOT need to regenerate your id_rsa_archerum key when switching from the 4-cab to 23-cab ARCHER2 system.' %}

### 1. Set up PUMA environment
If this is the first time you have used your PUMA account, you will need to create a `.profile` \\
Copy our standard one:
~~~
puma$ cd ~
puma$ cp ~um/um-training/setup/.profile .
~~~
(If you already have a `.profile`, make sure it includes the lines from the standard file.)

### 2. Generate authentication key for use with Rose/Cylc suites and the UMUI
Due to ARCHER2 being 2-factor authentication we have to use a separate ssh-key which is only used for submitting suites/jobs from PUMA. Run the following command to generate your `archerum` ssh key.
~~~
puma$ ssh-keygen -t rsa -b 4096 -C "ARCHER2 UM Workflow" -f ~/.ssh/id_rsa_archerum
~~~
When prompted to "Enter passphrase", this should be a fairly complicated and unguessable passphrase. You can use spaces in the passphrase if it helps you to remember it more readily. It is recommended that you don’t use your password in case it is hacked.

Your `id_rsa_archerum` key will be automatically picked up and sent to ARCHER2 to install. It may take up to 48 hours, excluding weekends, to become activated on ARCHER2.

{% include alert important="Important:<br> DO NOT use an empty passphrase as this presents a security issue. <br> DO NOT regenerate your archerum ssh-key once you have a working one in place, unless absolutely necessary.<br> It may take up to 48 hours, excluding weekends, for your new key to be installed on ARCHER2." %}

### 3. Update ssh config file
In your PUMA `~/.ssh/config` file add the following section:
~~~
Host login*.archer2.ac.uk
User <archer2_username>
IdentityFile ~/.ssh/id_rsa_archerum
ForwardX11 no
ForwardX11Trusted no
~~~
Where `<archer2_username>` should be replaced with your ARCHER2 username.

### 4. Set up ssh-agent
Setting up ssh-agent allows caching of your `archerum` key passphrase for a period of time.
~~~
puma$ cp ~um/um-training/setup/ssh-setup ~/.ssh
~~~
Logout of PUMA and then back in again.

Add your `archerum` key to your ssh-agent by running:
~~~
puma$ ssh-add ~/.ssh/id_rsa_archerum
Enter passphrase for /home/<puma-username>/.ssh/id_rsa:
[TYPE_YOUR_PASSPHRASE]
~~~
You will be prompted for your passphrase.

The ssh agent should keep running even when you log out of PUMA, however it may stop from time to time, for example if PUMA is rebooted.

### 5. Verify the setup is correct
**Note:** Only proceed to this step once your archerum key has been installed on ARCHER2.

Try logging into ARCHER with:
~~~
puma$ ssh login.archer2.ac.uk
~~~
You should NOT be prompted for your passphrase. The response from ARCHER2 should be similar to:
~~~
PTY allocation request failed on channel 0
Comand rejected by policy. Not in authorised list
Connection to login.archer2.ac.uk closed.
~~~
