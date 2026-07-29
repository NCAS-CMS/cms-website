---
layout: page-fullwidth
title:  "People"
#subheadline:  "Headers With Style"
teaser: "Meet the NCAS-CMS team."
permalink: "/people/"
categories:
    - design
tags:
    - design
    - background color
    - header

---
{% assign heads = site.data.people | where:'head',true %}
{% for person in heads -%}
| [{{ person.firstname }} {{ person.lastname }}](https://ncas.ac.uk/people/{{ person.ncas_id }}/{{ person.firstname | downcase }}-{{ person.lastname | downcase }}){:target="_blank"} | {{ person.position }} |
{% endfor -%}

{% assign people = site.data.people | sort: 'lastname' %}
{%- for person in people -%}
 {%- if person.head != true -%}
| [{{ person.firstname }} {{ person.lastname }}](https://ncas.ac.uk/people/{{ person.ncas_id }}/{{ person.firstname | downcase }}-{{ person.lastname | downcase }}){:target="_blank"} | {{ person.position }} |
 {% endif -%}
{% endfor %}



