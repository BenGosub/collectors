# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import requests
import sqlalchemy
import os
from datetime import date, timedelta
import time
import six
from .. import base
from .parser import parse_response


parse_datetime = base.helpers.parse_datetime

url = os.environ.get('HRA_URL')
hra_user = os.environ.get('HRA_USERNAME')
hra_pass = os.environ.get('HRA_PASSWORD')

s = requests.Session()

# Module API


def collect(conf, conn):
    errors = 0
    success = 0
    try:
        table = conn['warehouse'].load_table('hra')
        if table.count() == 0:
            to_date = date.today()
        else:
            to_date = _get_to_date()

    except sqlalchemy.exc.NoSuchTableError:
        to_date = date.today()

    query_period = 6
    from_date = to_date - timedelta(days=query_period)
    response, endpoint = _make_request(from_=from_date, to=to_date, url=url, filter=None)
    record = parse_response(response, endpoint, from_date, to_date, errors, success)
    base.writers.write_record(conn, record)

    if (len(response.json()) > 0):
        while True:
            to_date = _get_to_date()
            from_date = to_date - timedelta(days=query_period)
            logger.info('Sleeping for 30sec.')
            time.sleep(30)
            response, endpoint = _make_request(from_=from_date, to=to_date, url=url, filter=None)
            record = parse_response(response, endpoint, from_date, to_date, errors, success)
            base.writers.write_record(conn, record)

# Internal


def _make_request(url, from_, to, filter=None):
    # Updates filter is optional-categorical value
    # 1 - returns all studies for the given period
    # 2 - returns only studies published in the period
    # 3 - returns only studies modified in the period
    result_str = '{0}?datePublishedFrom={1}&datePublishedTo={2}'.format(url, from_, to)
    if filter is None:
        pass
    else:
        result_str = result_str + '&updatesFilter={}'.format(six.u(str(filter)))
    response = s.get(result_str, auth=(hra_user, hra_pass))
    return (response, result_str)


def _get_to_date(conn):
        to_date = conn['warehouse'].query('select min(api_date_from) from hra').result_proxy.first()[0] - timedelta(days=1)
        return to_date
