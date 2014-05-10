# -*- coding: utf-8 -*-

import pytest


def get_MUT():
    from bookmatch.crawler import sinkan as m
    return m


class TestSinkanCrawler(object):

    def get_class(self):
        return get_MUT().SinkanCrawler

    def test_init(self):
        cls = self.get_class()
        crawler = cls(2014, 1, 1)

    @pytest.mark.skip
    def test_crawl(self):
        # ToDo
        pass
