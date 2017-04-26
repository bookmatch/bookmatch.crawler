# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import urllib

import feedparser

__all__ = ['HanmotoRssCrawler']


class HanmotoRssCrawler(object):
    def crawl(self):
        url = "http://www.hanmoto.com/ci/bd/search/sdate/today/edate/today/hdt/{0}/vw/rss20".format(urllib.quote(u"新しい本".encode('utf-8')))

        data = feedparser.parse(url)
        for entry in data['entries']:
            link = entry['link']
            m = re.match(r'^.*/isbn/(\d{13})$', link)
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

