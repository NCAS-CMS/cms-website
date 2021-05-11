---
layout: page-fullwidth
title: Current Projects
subheadline: Projects
teaser: CMS provides direct-funded and un-funded support for a range of projects.
permalink: /services/projects/
---
{% assign current = site.projects | where: 'status', 'active' %}
{% assign funded = current | where: 'type','funded' %}
<h3>Funded</h3>
<ul>
  {% for project in funded %}
    <li>
      <b><a href="{{ project.url | relative_url }}">{{ project.title }}</a></b>
      {{ project.teaser | markdownify }}
    </li>
  {% endfor %}
</ul>

{% assign core = current | where: 'type','core' %}
<h3>Core</h3>
<ul>
  {% for project in core %}
    <li>
      <b><a href="{{ project.url | relative_url }}">{{ project.title }}</a></b>
      {{ project.teaser | markdownify}}
    </li>
  {% endfor %}
</ul>

