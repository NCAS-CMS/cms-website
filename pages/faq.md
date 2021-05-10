---
layout: page
show_meta: false
title: "Frequently Asked Questions"
#subheadline: "Layouts of Feeling Responsive"
#header:
#   image_fullwidth: "header_unsplash_5.jpg"
permalink: "/faq/"
---
{% comment %}
<ul>
    {% for post in site.categories.faq %}
    <li><a href="{{ site.url }}{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>
{% endcomment %}

{% assign sorted_tags = site.tags | sort %}
{% for tag in sorted_tags %}
  {% assign tag_posts = tag[1] | where: "categories", "faq" | sort %}
  {% if tag_posts != empty %}
  <h3>{{ tag[0] | upcase }}</h3>
  <ul>
    {% for post in tag_posts %}
    <li><a href="{{ site.url }}{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
  {% endif %}
{% endfor %}



