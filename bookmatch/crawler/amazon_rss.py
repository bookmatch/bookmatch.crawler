# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import datetime
from bookmatch.crawler.compat import urlsplit

import feedparser
import lxml.html

from bookmatch.crawler.util import normalize_isbn13

__all__ = ['AmazonRssCrawler']


class AmazonRssCrawler(object):
    def __init__(self, category='books', domain='.co.jp'):
        self.rss_url = \
            "http://www.amazon{domain}/gp/rss/new-releases/{category}".format(
            category=category, domain=domain)

    def crawl(self):
        data = feedparser.parse(self.rss_url)
        for entry in data['entries']:
            link = entry['link']
            m = re.search(r'/dp/([0-9X]{10})/', urlsplit(link)[2])
            if m is None:
                continue
            asin = m.group(1)
            try:
                isbn = normalize_isbn13(asin)
            except ValueError:
                continue
            title = re.sub(r'#\d+:\s*', '', entry['title'])
            summary = lxml.html.fromstring(entry['summary'])
            nodes = summary.cssselect('span.riRssContributor')
            if len(nodes) == 1:
                author = nodes[0].text_content()
            else:
                author = None
            # relrease_date = summary.cssselect('span.riRssReleaseDate')[0].text_content()
            # published = datetime.datetime(*entry['published_parsed'][:6])
            yield {
                'isbn': isbn,
                'title': title,
                'author': author,
                }


if __name__ == '__main__':
    crawler = AmazonRssCrawler()
    for d in crawler.crawl():
        print(d['isbn'], d['title'])
