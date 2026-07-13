---
layout: page
title: 随笔
permalink: /essays/
---

{% assign posts = site.categories.essay %}

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
  <p>还没有 essay 分类的文章。</p>
{% endif %}
