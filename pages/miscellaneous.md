---
layout: page-fullwidth
title: Miscellaneous Documents
subheadline: Documentation 
teaser: Collection of miscellaneous documents.
permalink: /miscellaneous/
---
{% assign docs = site.miscellaneous %}


<ul>
  {% for doc in docs %}
    <li>
      <b><a href="{{ doc.url | relative_url }}">{{ doc.title }}</a></b>
      {{ doc.teaser | markdownify }}
    </li>
  {% endfor %}
</ul>


