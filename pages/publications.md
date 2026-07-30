---
layout: page-fullwidth
title: Posters, Presentations & Publications
teaser: NCAS-CMS frequently attend workshops and conferences giving talks and presenting posters as well as writing papers. 
permalink: /presentations-and-publications/
---
<div>
  {% for year in site.data.publications %}

    {% comment %} 1. Handle legacy nested structure {% endcomment %}
    {% if year.publication_type %}
      {% assign valid_docs_count = 0 %}
      {% for entry in year.publication_type %}
        {% unless entry.type == "Presentations" %}
          {% if entry.docs.size > 0 %}
            {% assign valid_docs_count = valid_docs_count | plus: entry.docs.size %}
          {% endif %}
        {% endunless %}
      {% endfor %}

      {% comment %} Only display the year header if there are non-presentation docs {% endcomment %}
      {% if valid_docs_count > 0 %}
        <h3>{{ year.year }}</h3>
        {% for entry in year.publication_type %}
          {% unless entry.type == "Presentations" %}
            {% if entry.type != "Publications" %}
              <b>{{ entry.type }}</b>
            {% endif %}
            {% if entry.docs %}
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
          {% endunless %}
        {% endfor %}
      {% endif %}

    {% comment %} 2. Handle flat structure from Python script {% endcomment %}
    {% elsif year.docs and year.docs.size > 0 %}
      <h3>{{ year.year }}</h3>
      <ul>
      {% for item in year.docs %}
        {% if item.url %}
          <li>{{ item.authors }}; <a href="{{ item.url }}">{{ item.title }}</a>; {{ item.location }}</li>
        {% else %}
          <li>{{ item.authors }}; <a href="{{ site.url }}{{ site.baseurl }}/assets/docs/{{ item.file }}">{{ item.title }}</a>; {{ item.location }}</li>
        {% endif %}
      {% endfor %}
      </ul>
    {% endif %}

  {% endfor %}
</div>
