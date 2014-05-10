# -*- coding: utf-8 -*-

import sys

__all__ = [
    'urlencode',
    'parse_qsl',
    'urlsplit',
]

py2 = sys.version_info < (3, 0, 0)

if py2:
    from urllib import urlencode
    from urlparse import parse_qsl, urlsplit
else:
    from urllib.parse import (
        urlencode,
        parse_qsl,
        urlsplit,
        )
