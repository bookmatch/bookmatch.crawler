# -*- coding: utf-8 -*-

import pytest


def get_MUT():
    from bookmatch.crawler import hanmoto_rss as m
    return m


class TestHanmotoRssCrawler(object):

    def get_class(self):
        return get_MUT().HanmotoRssCrawler

    def test_init(self):
        cls = self.get_class()
        crawler = cls()

    @pytest.mark.skip
    def test_crawl(self):
        # ToDo
        pass
