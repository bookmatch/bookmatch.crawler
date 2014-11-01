# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import datetime

from bookmatch.crawler import models
from bookmatch.crawler.models import DBSession, Content

from bookmatch.crawler.sinkan import SinkanCrawler

logger = None

crawler_classes = {
    'sinkan_web': SinkanCrawler,
}


def main(config, date):
    crawlers = []
    for name, crawler_cls in crawler_classes.items():
        logger.info("crawling %s...", name)
        crawler = crawler_cls(date.year, date.month, date.day, wait=5.0)
        added = modified = 0
        n = 0
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
            n += 1
            if n >= 100:
                DBSession.commit()
                n = 0
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
    logging.getLogger('requests.packages.urllib3.connectionpool') \
        .setLevel(logging.WARN)


def parse_date(s):
    try:
        dt = datetime.datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        dt = datetime.datetime.strptime(s, '%Y%m%d')
    return dt.date()


if __name__ == '__main__':
    import sys
    from ConfigParser import SafeConfigParser
    p = SafeConfigParser()
    p.read(sys.argv[1])

    config = dict(p.items('bookmatch.crawler'))

    if len(sys.argv) > 2:
        date = parse_date(sys.argv[2])
    else:
        date = datetime.date.today()

    configure_logging(config)
    configure_db(config)
    main(config, date)
