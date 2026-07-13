---
layout: page
title: 归档
permalink: /archive/
---

{% assign year = '' %}
{% for post in site.posts %}
{% assign current_year = post.date | date: '%Y' %}
{% if current_year != year %}
{% assign year = current_year %}
{% unless forloop.first %}</ul>{% endunless %}
<h2>{{ year }}</h2>
<ul>
{% endif %}
<li>
  <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
  <small>{{ post.date | date: '%Y-%m-%d' }}</small>
</li>
{% if forloop.last %}</ul>{% endif %}
{% endfor %}
