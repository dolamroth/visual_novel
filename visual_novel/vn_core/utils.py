import json
import socket
import logging
import urllib3

from django import apps
from django.conf import settings

__version__ = '0.1'

vn_logger = logging.getLogger('vn_logger')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VndbStats(object):
    def __init__(self):
        self.sock = None
        self.protocol = settings.VNDB_API_PROTOCOL
        self.client = settings.VNDB_API_CLIENT
        self.clientver = settings.VNDB_API_CLIENTVER
        self.username = settings.VNDB_API_USERNAME
        self.password = settings.VNDB_API_PASSWORD
        self.eot = u"\u0004"

    class VndbError(Exception):
        message = ''

        def __str__(self):
            return self.message

    class VndbAuthError(VndbError):
        message = 'Подключение не выполнено'

    class VndbTypeError(VndbError):
        message = 'Передано значение неверного типа'

    def __assert(self, param, type):
        try:
            assert type(param), type
        except AssertionError:
            raise self.VndbTypeError()

    def login(self):
        HOST, PORT = settings.VNDB_API_HOST, settings.VNDB_API_PORT

        vndblogin = dict()

        vndblogin["protocol"] = self.protocol
        vndblogin["client"] = self.client
        vndblogin["clientver"] = self.clientver
        vndblogin["username"] = self.username
        vndblogin["password"] = self.password

        bindata = ("login " + json.dumps(vndblogin))

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.sock.sendall(bytes(bindata + self.eot, "utf-8"))
            # Read the response "Ok" in order to clear pipe for next call
            received = str(self.sock.recv(1024), "utf-8")
        except:
            self.sock = None
            raise self.VndbAuthError()

    def logout(self):
        try:
            self.sock.close()
        except:
            pass

    def update_vn(self, vndb_id):
        self.__assert(vndb_id, int)
        if self.sock is None:
            raise self.VndbAuthError()
        bindata = 'get vn stats (id = {})'.format(vndb_id)
        self.sock.sendall(bytes(bindata + self.eot, "utf-8"))
        received = str(self.sock.recv(1024), "utf-8")

        # The answer is always in format "results %json_object%" + terminate symbol u"\u0004"
        vn_obj = json.loads(received[8:-1])
        rating = round(float(vn_obj['items'][0]['rating']) * 100.0)
        popularity = round(float(vn_obj['items'][0]['popularity']) * 100.0)
        vote_count = round(vn_obj['items'][0]['votecount'])
        return rating, popularity, vote_count


class YandexMetrica(object):
    def __init__(self):
        self.token = settings.YANDEX_METRIKA_TOKEN
        self.client_id = settings.YANDEX_METRIKA_CLIENT_ID
        self.api_url = settings.YANDEX_METRIKA_URL
        self.method = 'GET'
        self.list_of_top_pages = None

    def __execute_query(self, query, params_q):
        params = dict(params_q)
        params['ids'] = self.client_id
        params['oauth_token'] = self.token
        url = self.api_url + query

        http = urllib3.PoolManager()
        r = http.request(self.method, url, fields=params)
        try:
            return json.loads(r.data)
        except json.decoder.JSONDecodeError:
            vn_logger.error('YANDEX METRIKA API returned {}'.format(r.data))

    def get_top_pages_for_period(self, date_from, date_to, max_result):
        query_url = 'stat/v1/data'
        params = dict()
        # TODO: Validation for correct "date_" and "max_result" format
        params['date1'] = date_from
        params['date2'] = date_to
        params['limit'] = max_result
        params['metrics'] = 'ym:pv:pageviews'
        params['dimensions'] = 'ym:pv:URLPathFull,ym:pv:title'
        params['sort'] = '-ym:pv:pageviews'
        self.list_of_top_pages = self.__execute_query(query=query_url, params_q=params)
        return self.list_of_top_pages
