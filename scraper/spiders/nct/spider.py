# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .. import base
from . import utils
from .parser import NctParser


# Module API

class NctSpider(base.Spider):

    # Public

    name = 'nct'
    allowed_domains = ['clinicaltrials.gov']

    def __init__(self, date_from=None, date_to=None, *args, **kwargs):

        # Create parser
        self.parser = NctParser()

        # Make start urls
        self.start_urls = utils.make_start_urls(
                prefix='https://www.clinicaltrials.gov/ct2/results',
                date_from=date_from, date_to=date_to)

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow=r'ct2/show/NCT\d+',
                process_value=lambda value: value+'&resultsxml=true',
            ), callback=self.parser.parse),
            Rule(LinkExtractor(
                allow=r'pg=\d+$',
            )),
        ]

        # Inherit parent
        super(NctSpider, self).__init__(*args, **kwargs)
