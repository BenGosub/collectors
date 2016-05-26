# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import requests
import sqlalchemy
import os
from datetime import date, timedelta, datetime, time
import time as tm
import six
from .. import base
from .parser import parse_response
import logging
import sys
logger = logging.getLogger(__name__)

url = os.environ.get('HRA_URL')
hra_user = os.environ.get('HRA_USERNAME')
hra_pass = os.environ.get('HRA_PASSWORD')
hra_dev_env = os.environ.get('HRA_DEVELOPMENT_ENVIRONMENT')

s = requests.Session()

# Module API


def collect(conf, conn):
    utc_now = datetime.utcnow()
    if hra_dev_env == 'STAGING':
        _collect_records(conn, url)
    else:
        if (utc_now.weekday() in [1, 3, 4] and utc_now.time() > time(6, 0) and utc_now.time() < time(8, 0)):
            _collect_records(conn, url)
        else:
            logger.warning('Time is not between 6-8 UTC and development set up is PRODUCTION, Sleeping for 1 hour')
            tm.sleep(60 * 60)
            sys.exit()


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
        result_str = '{0}&updatesFilter={1}'.format(result_str, six.u(str(filter)))
    response = s.get(result_str, auth=(hra_user, hra_pass))
    return response


def _get_from_date(conn):
    from_date = conn['warehouse'].query('select max(publication_date) from hra').result_proxy.first()[0] + timedelta(days=1)
    return from_date


def _collect_records(conn, url):
    errors = 0
    success = 0
    beginning_date = date(2008, 12, 1)
    last_updated_iter = conn['warehouse'].query('select max(meta_updated) from hra')
    for row in last_updated_iter:
        last_updated = row['max'].date()
    try:
        table = conn['warehouse'].load_table('hra')
        if table.count() == 0:
            # If no records found, start at the beginning
            from_date = beginning_date
        else:
            from_date = _get_from_date(conn)

    except sqlalchemy.exc.NoSuchTableError:
        # Start from the begining where first record is found
        from_date = beginning_date

    query_period = 24
    to_date = from_date + timedelta(days=query_period)
    while to_date < date.today():
        response = _make_request(from_=from_date, to=to_date, url=url, filter=None)
        if (len(response.json()) > 0):
            for application in response.json():
                try:
                    record = parse_response(application, response, last_updated)
                    base.writers.write_record(conn, record)
                    success += 1
                    if not success % 100:
                        logger.info('Collected %s "%s" applications',
                            success, record.table)
                except Exception as exception:
                    # Log warning
                    errors += 1
                    logger.warning('Collecting error: %s', repr(exception))
        from_date = to_date + timedelta(days=1)
        to_date = to_date + timedelta(days=query_period)
        logger.info('Sleeping for 30sec.')
        tm.sleep(30)
