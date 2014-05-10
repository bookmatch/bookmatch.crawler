# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
from time import sleep
from bookmatch.crawler.compat import parse_qsl, urlsplit, urlencode

import lxml.html
import requests

from bookmatch.crawler.util import normalize_isbn13

__all__ = ['SinkanCrawler']


class SinkanCrawler(object):
    default_categories = ["Book"]

    def __init__(self, year, month, day, wait=3.0, categories=None):
        self.year = year
        self.month = month
        self.day = day
        self.wait = wait

        if categories is None:
            categories = self.default_categories
        self.categories = categories

    def crawl(self):
        base_url = "http://sinkan.net/?"

        start = "{0:04d}-{1:02d}-{2:02d}".format(
            self.year, self.month, self.day)
        base_query = {
            "action_top": "true",
            "start": start,
            }

        offset = 0
        while True:
            params = dict(base_query, offset=offset)
            url = base_url + urlencode(params)
            r = requests.get(url)
            doc = lxml.html.fromstring(r.content)
            for table in doc.cssselect('table.item_simple'):
                tags = [img.attrib.get('alt')
                        for img in table.cssselect('.i_store img')]
                if not set(tags).intersection(self.categories):
                    continue
                a = table.cssselect('.i_info .i_title a')[0]
                title = a.text
                href = a.attrib.get('href')
                asin = dict(parse_qsl(urlsplit(href)[3]))['asin']
                try:
                    isbn = normalize_isbn13(asin)
                except ValueError:
                    continue
                author = table.cssselect('.i_author')[0].text
                yield {
                    'isbn': isbn,
                    'title': title,
                    'author': author,
                    }
            offset += 60
            if len(doc.cssselect('a[rel=next]')) == 0:
                break
            sleep(self.wait)


if __name__ == '__main__':
    today = datetime.date.today()
    crawler = SinkanCrawler(today.year, today.month, today.day)
    for d in crawler.crawl():
        print(d['isbn'], d['title'])
