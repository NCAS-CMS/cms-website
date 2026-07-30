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

      {% if valid_docs_count > 0 %}
        {% comment %} Removed year heading: <h3>{{ year.year }}</h3> {% endcomment %}
        {% for entry in year.publication_type %}
          {% unless entry.type == "Presentations" %}
            {% if entry.type != "Publications" %}
              <b>{{ entry.type }}</b>
            {% endif %}
            {% if entry.docs %}
              <ul>
              {% for item in entry.docs %}
                {% assign author_val = item.authors | default: item.author %}
                <li>
                  {% if author_val %}{{ author_val }}; {% endif %}
                  {% if item.url %}
                    <a href="{{ item.url }}">{{ item.title }}</a>
                  {% elsif item.file %}
                    <a href="{{ site.url }}{{ site.baseurl }}/assets/docs/{{ item.file }}">{{ item.title }}</a>
                  {% else %}
                    {{ item.title }}
                  {% endif %}
                  {% if item.location %}; {{ item.location }}{% endif %}
                </li>
              {% endfor %}
              </ul>
            {% endif %}
          {% endunless %}
        {% endfor %}
      {% endif %}

    {% comment %} 2. Handle flat structure from Python script {% endcomment %}
    {% elsif year.docs and year.docs.size > 0 %}
      {% comment %} Removed year heading: <h3>{{ year.year }}</h3> {% endcomment %}
      <ul>
      {% for item in year.docs %}
        {% assign author_val = item.authors | default: item.author %}
        <li>
          {% if author_val %}{{ author_val }}; {% endif %}
          {% if item.url %}
            <a href="{{ item.url }}">{{ item.title }}</a>
          {% elsif item.file %}
            <a href="{{ site.url }}{{ site.baseurl }}/assets/docs/{{ item.file }}">{{ item.title }}</a>
          {% else %}
            {{ item.title }}
          {% endif %}
          {% if item.location %}; {{ item.location }}{% endif %}
        </li>
      {% endfor %}
      </ul>
    {% endif %}

  {% endfor %}
</div>
