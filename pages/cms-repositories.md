---
layout: page-fullwidth
title: CMS Public Repositories
permalink: /repos/
---
{% for repository in site.github.public_repositories %}
  * [{{ repository.name }}]({{ repository.html_url }})
{% endfor %}
