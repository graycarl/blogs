#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'hongbo'
SITENAME = u'HHBCARL'
SITEURL = ''

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
# FEED_ALL_RSS = "feeds/all.rss.xml"
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python China', 'http://python-china.org/'))

# Social widget
SOCIAL = (('GitHub', 'http://github.com/graycarl'),
        ('Weibo', 'http://weibo.com/graycarl'),)

DEFAULT_PAGINATION = 10

FILES_TO_COPY = (('extra/CNAME', 'CNAME'),)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
