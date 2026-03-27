---
layout: default
title: Blog
permalink: /blog/
---

# Blog

Analysis, commentary, and proposals on the EU data law landscape.

{% for post in site.posts %}
### [{{ post.title }}]({{ post.url | relative_url }})
<small>{{ post.date | date: "%B %-d, %Y" }}</small>

{{ post.excerpt }}

---
{% endfor %}
