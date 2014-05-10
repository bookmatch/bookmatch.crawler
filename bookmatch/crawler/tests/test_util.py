# -*- coding: utf-8 -*-

import pytest
from testfixtures import compare


def get_MUT():
    from bookmatch.crawler import util as m
    return m


def TestIsbn13Digit(object):

    def get_FUT(self):
        return get_MUT().isbn13_digit

    @pytest.mark.parametrize("digits,expect", [
            ("978410109205", "8"),
            ("978493901580", "9"),
            ("978400310101", "8"),
            ])
    def test_it(digits, expect):
        target = self.get_FUT()
        compare(target(digits), expect)


class TestNormalizeIsbn13(object):

    def get_FUT(self):
        return get_MUT().normalize_isbn13

    def test_isbn13(self):
        target = self.get_FUT()
        compare(target("9784003101018"), "9784003101018")

    def test_isbn13_with_hyphen(self):
        target = self.get_FUT()
        compare(target("978-4-00-310101-8"), "9784003101018")

    def test_isbn10(self):
        target = self.get_FUT()
        compare(target("4003101014"), "9784003101018")

    def test_isbn10_with_hyphen(self):
        target = self.get_FUT()
        compare(target("4-00-310101-4"), "9784003101018")
