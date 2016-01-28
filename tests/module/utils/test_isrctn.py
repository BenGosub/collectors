# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from importlib import import_module
module = import_module('scraper.utils.isrctn')


def test_make_start_urls():
    result = module.make_start_urls('prefix', '2016-01-01', '2016-01-15')
    print(result)
    assert result


def test_make_pattetn():
    result = module.make_pattern('prefix')
    print(result)
    assert result
