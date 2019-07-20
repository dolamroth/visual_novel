import urllib3
import json
import logging
import time
from timeit import default_timer as timer

from django.conf import settings


def addr_query_yandex(query):

    http = urllib3.PoolManager()

    yandex_logger = logging.getLogger('vn_logger')

    start = timer()
    r = http.request(
        "GET",
        "http://geocode-maps.yandex.ru/1.x/",
        fields={
            "format": "json",
            "geocode": query,
        },
        headers={
            "Accept": "application/json",
            "User-agent": "visual novel bot"
        }
    )
    end = timer()

    yandex_logger.info('Query to yandex with query "{}" took {} seconds to proceed with status {}'
                       .format(query, end - start, r.status))

    return json.loads(r.data.decode('utf-8'))
