# -*- coding: utf-8 -*-

from __future__ import print_function

import re

import feedparser

__all__ = ['HanmotoRssCrawler']


class HanmotoRssCrawler(object):
    def crawl(self):
        url = "http://www.hanmoto.com/jpokinkan/rss/uptodate.xml"

        data = feedparser.parse(url)
        for entry in data['entries']:
            link = entry['link']
            m = re.match(r'^.*/(\d{13})\.html$', link)
            if m is None:
                continue
            isbn = m.group(1)
            title = entry['title']
            yield {
                'isbn': isbn,
                'title': title,
                }


if __name__ == '__main__':
    crawler = HanmotoRssCrawler()
    for d in crawler.crawl():
        print(d['isbn'], d['title'])

