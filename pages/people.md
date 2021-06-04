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

{% assign people = site.data.people | sort: 'lastname' %}
{% for person in people -%}
| [{{ person.firstname }} {{ person.lastname }}](https://ncas.ac.uk/people/{{ person.ncas_id }}/{{ person.firstname | downcase }}-{{ person.lastname | downcase }}) | {{ person.position }} |
{% endfor %}

{% comment %}
| [Bryan Lawrence](https://ncas.ac.uk/people/10008/bryan-lawrence) | Director of Models and Data |
| [Grenville Lister](https://ncas.ac.uk/people/10170/grenville-lister) | Head of NCAS Computational Modelling Services |
| [Luke Abraham](https://ncas.ac.uk/people/10166/nathan-abraham) | UKCA development and support |
| [Fanny Adloff](https://ncas.ac.uk/people/10514/fanny-adloff) | EU Project Scientific Officer (IS-ENES3) |
| [Sadie Bartholomew](https://ncas.ac.uk/people/10515/sadie-bartholomew) | CF-Python & ES-DOC (IS-ENES3) |
| [David Case](https://ncas.ac.uk/people/10466/david-case) | Software infrastructure and modelling support |
| [Jeff Cole](https://ncas.ac.uk/people/10105/jeff-cole) | Model support and software tools specialist |
| [Thibault Hallouin](https://ncas.ac.uk/people/10505/thibault%20-hallouin) | Hydro-JULES |
| [David Hassell](https://ncas.ac.uk/people/10288/david-hassell) | Software tools specialist – CF-Python - IS-ENES3 |
| [Rosalyn Hatcher](https://ncas.ac.uk/people/10106/rosalyn-hatcher) | NCAS HPC Manager, Software Management & Infrastructure |
| [Andy Heaps](https://ncas.ac.uk/people/10107/andy-heaps) | System administration and visualisation specialist |
| [Patrick McGuire](https://ncas.ac.uk/people/10443/patrick-mcguire) | Land surface modelling development and support |
| [Annette Osprey](https://ncas.ac.uk/people/10171/annette-osprey) | High Resolution Climate Modelling support |
| [Valeriu Predoi](https://ncas.ac.uk/people/10412/valeriu-predoi) | UKESM core team: diagnostic software |
| [Marc Stringer](https://ncas.ac.uk/people/10320/marc-stringer) | UKESM core team: performance |
| [Simon Wilson](https://ncas.ac.uk/people/10108/simon-wilson) | Model support and performance specialist |
{% endcomment %}


