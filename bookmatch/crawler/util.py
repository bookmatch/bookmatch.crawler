# -*- coding: utf-8 -*-

__all__ = [
    'isbn13_digit',
    'normalize_isbn13',
]


def isbn13_digit(digits):
    if len(digits) != 12:
        raise ValueError(digits)
    tmp = sum([(i % 2 and 3 or 1) * int(n) for i, n in enumerate(digits)])
    return str(-tmp % 10)


def normalize_isbn13(isbn):
    isbn = isbn.replace('-', '')
    if len(isbn) == 10:
        isbn = '978' + isbn[:9]
        isbn += isbn13_digit(isbn)
    return isbn
