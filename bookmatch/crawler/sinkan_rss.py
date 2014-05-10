# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import datetime
from bookmatch.crawler.compat import parse_qsl, urlsplit

import feedparser

from bookmatch.crawler.util import normalize_isbn13

__all__ = ['SinkanRssCrawler']


class SinkanRssCrawler(object):
    default_categories = ["Book"]

    def __init__(self, categories=None):
        if categories is None:
            categories = self.default_categories
        self.categories = categories

    def crawl(self):
        url = "http://sinkan.net/?action_rss=true&mode=today"
        data = feedparser.parse(url)
        for entry in data['entries']:
            tags = [tag['term'] for tag in entry['tags']]
            if not set(tags).intersection(self.categories):
                continue
            link = entry['link']
            asin = dict(parse_qsl(urlsplit(link)[3]))['asin']
            try:
                isbn = normalize_isbn13(asin)
            except ValueError:
                continue
            title = re.sub(r'^\d{4}-\d{2}-\d{2}\s*', '', entry['title'])
            # published = datetime.datetime(*entry['published_parsed'][:6])
            yield {
                'isbn': isbn,
                'title': title,
                }


if __name__ == '__main__':
    crawler = SinkanRssCrawler()
    for d in crawler.crawl():
        print(d['isbn'], d['title'])
