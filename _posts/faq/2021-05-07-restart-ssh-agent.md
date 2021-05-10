---
layout: page
subheadline:  "SSH"
title:  "How do I restart my ssh-agent?"
teaser: "Normally your `ssh-agent` persists even when you log out of a machine.  However, from time to time, it can stop and will need restating."
categories:
    - faq
tags:
    - puma 
author: ros
#header: no
---
If you are prompted for your passphrase, this means the `ssh-agent` has stopped for some reason. The agent should have been re-initialised when you logged onto PUMA and you will need to re-associate your ssh keys to the agent.

To do so, run the command:

`puma$ ssh-add`

{% comment %} Leave below here {% endcomment %}
## All FAQ Items
{: .t60 }

{% include list-posts category='faq' %}
