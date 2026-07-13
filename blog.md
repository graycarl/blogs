---
layout: page
title: 博客
permalink: /blog/
---

{% assign posts = site.categories.blog %}

{% if posts and posts.size > 0 %}
  <ul>
    {% for post in posts %}
      <li>
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        <small>{{ post.date | date: '%Y-%m-%d' }}</small>
      </li>
    {% endfor %}
  </ul>
{% else %}
  <p>还没有 blog 分类的文章。</p>
{% endif %}
