#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'hongbo'
SITENAME = u'Hongbo He'
SITESUBTITLE = u'月亮哪去了'
SITEURL = ''
# DISQUS_SITENAME = "blog.graycarl.me"
DUOSHUO_SITENAME = "carlblog"

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'en'

DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MEUN = False

# Baidu Tongji
BAIDU_TONGJI = True

# Feed generation is usually not desired when developing
# FEED_ALL_RSS = "feeds/all.rss.xml"
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python China', 'http://python-china.org/'))

# Social widget
SOCIAL = (('GitHub', 'http://github.com/graycarl'),
          ('Weibo', 'http://weibo.com/graycarl'),)

DEFAULT_PAGINATION = 10
SUMMARY_MAX_LENGTH = 20

FILES_TO_COPY = (('extra/CNAME', 'CNAME'),
                 ('resources/hhbavatar.jpg', 'hhbavatar.jpg'))

# THEME = "/Users/carl/source/pelican-subtle/"
THEME = "/Users/carl/source/pelican-hhb/"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
