---
layout: page-fullwidth
title: Posters, Presentations & Publications
teaser: NCAS-CMS frequently attend workshops and conferences giving talks and presenting posters as well as writing papers. Here you will find our recent publications.
permalink: /presentations-and-publications/
---
<div>
  {% for year in site.data.publications %}
    <h3>{{ year.year }}</h3>
    {% if year.publication_type[0] %}
      {% for entry in year.publication_type %}
        <b>{{ entry.type }}</b>
        {% if entry.docs[0] %}
          <ul>
          {% for item in entry.docs %}
              {% if item.url %}
                <li>{{ item.authors }}; <a href="{{ item.url }}">{{ item.title }}</a>; {{ item.location }}</li>
              {% else %}
                <li>{{ item.authors }}; <a href="{{ site.url }}{{ site.baseurl }}/assets/docs/{{ item.file }}">{{ item.title }}</a>; {{ item.location }}</li>
              {% endif %}
          {% endfor %}
          </ul>
        {% endif %}
      {% endfor %}
    {% endif %}
  {% endfor %}
</div>