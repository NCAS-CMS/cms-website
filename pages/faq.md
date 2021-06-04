---
layout: page
show_meta: false
title: "Frequently Asked Questions"
#subheadline: "Layouts of Feeling Responsive"
#header:
#   image_fullwidth: "header_unsplash_5.jpg"
permalink: "/user-support/faq/"
breadcrumb: true
---

{% assign items_grouped = site.faq | group_by: 'group' %}
{% for group in items_grouped %}
  <h3>{{ group.name | upcase }}</h3>
  <ul>
    {% for item in group.items %}
      <li><a href="{{ site.url }}{{ site.baseurl }}{{ item.url }}">{{ item.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}



