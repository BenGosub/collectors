# -*- coding: utf-8 -*-
# pylama:skip=1
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from urllib import urlencode
from datetime import date, timedelta
from collections import OrderedDict
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .. import items
from .. import helpers


# Module API

class Isrctn(CrawlSpider):

    # Public

    name = 'isrctn'
    allowed_domains = ['isrctn.com']

    def __init__(self, date_from=None, date_to=None, *args, **kwargs):

        # Make start urls
        self.start_urls = _make_start_urls(
                base='http://www.isrctn.com/search',
                date_from=date_from, date_to=date_to)

        # Make rules
        self.rules = [
            Rule(LinkExtractor(allow=_make_pattern('search'))),
            Rule(LinkExtractor(allow=r'ISRCTN\d+'), callback='parse_item'),
        ]

        # Inherit parent
        super(Isrctn, self).__init__(*args, **kwargs)

    def parse_item(self, res):

        # Create item
        item = items.Isrctn()

        # Get isrctn_id
        path = '.ComplexTitle_primary::text'
        item['isrctn_id'] = res.css(path).extract_first()

        # Get meta
        key = None
        value = None
        for sel in res.css('.Meta_name, .Meta_name+.Meta_value'):
            if sel.css('.Meta_name'):
                key = None
                value = None
                elements = sel.xpath('text()').extract()
                if elements:
                    key = helpers.slugify(elements[0].strip())
            else:
                if key is not None:
                    value = None
                    elements = sel.xpath('text()').extract()
                    if elements:
                        value = elements[0].strip()
            if key and value:
                item.add_data(key, value)

        # Get data
        key = None
        value = None
        for sel in res.css('.Info_section_title, .Info_section_title+p'):
            if sel.css('.Info_section_title'):
                key = None
                value = None
                elements = sel.xpath('text()').extract()
                if elements:
                    key = helpers.slugify(elements[0].strip())
            else:
                if key is not None:
                    value = None
                    elements = sel.xpath('text()').extract()
                    if elements:
                        value = elements[0].strip()
            if key and value:
                item.add_data(key, value)

        return item


# Internal

def _make_start_urls(base, date_from=None, date_to=None):
    """ Return start_urls.
    """
    if date_from is None:
        date_from = str(date.today() - timedelta(days=1))
    if date_to is None:
        date_to = str(date.today())
    query = OrderedDict()
    query['q'] = ''
    gtle = 'GT lastEdited:%sT00:00:00.000Z' % date_from
    lele = 'LE lastEdited:%sT00:00:00.000Z' % date_to
    query['filters'] = ','.join([gtle, lele])
    query['page'] = '1'
    query['pageSize'] = '100'
    query['searchType'] = 'advanced-search'
    return [base + '?' + urlencode(query)]


def _make_pattern(base):
    """ Return pattern.
    """
    pattern = base
    pattern += r'\?q=&filters=GT[^,]*,LE[^,]*&page=\d+&'
    pattern += r'pageSize=100&searchType=advanced-search$'
    return pattern
