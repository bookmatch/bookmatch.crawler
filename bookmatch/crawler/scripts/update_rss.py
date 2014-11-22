# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import datetime

from bookmatch.crawler import models
from bookmatch.crawler.models import DBSession, Content

from bookmatch.crawler.amazon_rss import AmazonRssCrawler
from bookmatch.crawler.hanmoto_rss import HanmotoRssCrawler
from bookmatch.crawler.sinkan_rss import SinkanRssCrawler

logger = None

crawler_classes = {
    'amazon': AmazonRssCrawler,
    'hanmoto': HanmotoRssCrawler,
    'sinkan': SinkanRssCrawler,
}


def run_crawler(crawler):
    added = modified = 0
    for d in crawler.crawl():
        content = Content.query \
            .filter_by(isbn=d['isbn'], source=name) \
            .first()
        if content is not None:
            # don't update
            continue
        else:
            content = Content(isbn=d['isbn'], source=name)
            DBSession.add(content)
            added += 1
        title = d['title']
        author = d.get('author') or u""
        if title == content.title and author == content.author:
            continue
        content.title = title
        content.author = author
        content.update_at = datetime.datetime.now()
        modified += 1
        print(content.isbn, content.title.encode('utf-8'))
    return added, modified


def main(config):
    crawlers = []
    for name, crawler_cls in crawler_classes.items():
        logger.info("crawling %s...", name)
        crawler = crawler_cls()
        try:
            added, modified = run_crawler(crawler)
        except Exception, e:
            logger.error(e)
            continue
        DBSession.commit()
        logger.info("added: %d, updated: %d", added, modified - added)


def configure_db(config, prefix='sqlalchemy.'):
    from sqlalchemy import engine_from_config
    engine = engine_from_config(config, prefix)
    DBSession.configure(bind=engine)
    models.Base.metadata.bind = engine
    models.Base.metadata.create_all()


def configure_logging(config):
    global logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%H:%M:%S")
    logger = logging.getLogger()


if __name__ == '__main__':
    import sys
    from ConfigParser import SafeConfigParser
    p = SafeConfigParser()
    p.read(sys.argv[1])

    config = dict(p.items('bookmatch.crawler'))

    configure_logging(config)
    configure_db(config)
    main(config)
