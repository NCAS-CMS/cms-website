---
layout: page-fullwidth
title: Previous Projects
subheadline: Projects
teaser: Previous projects that CMS have supported.
permalink: /services/archived-projects/
---
{% assign previous = site.projects | where: 'status', 'archived' %}
{% assign funded = previous | where: 'type','funded' %}
<h3>Funded</h3>
<ul>
  {% for project in funded %}
    <li>
      <b><a href="{{ project.url | relative_url }}">{{ project.title }}</a></b>
      {{ project.teaser | markdownify }}
    </li>
  {% endfor %}
</ul>

{% assign core = previous | where: 'type','core' %}
<h3>Core</h3>
<ul>
  {% for project in core %}
    <li>
      <b><a href="{{ project.url | relative_url }}">{{ project.title }}</a></b>>
      {{ project.teaser | markdownify }}
    </li>
  {% endfor %}
</ul>
