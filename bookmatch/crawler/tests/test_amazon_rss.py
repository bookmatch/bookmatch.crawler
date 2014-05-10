# -*- coding: utf-8 -*-

import pytest


def get_MUT():
    from bookmatch.crawler import amazon_rss as m
    return m


class TestAmazonCrawler(object):

    def get_class(self):
        return get_MUT().AmazonRssCrawler

    def test_init(self):
        cls = self.get_class()
        crawler = cls()

    @pytest.mark.skip
    def test_crawl(self):
        # ToDo
        pass
