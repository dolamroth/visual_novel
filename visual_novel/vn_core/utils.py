import datetime
import json
import socket
import logging
import urllib3

from django.apps import apps
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

    def __assert(self, param, expected_type):
        try:
            assert type(param) == expected_type
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
        self.list_of_top_pages_dict = None

        self.date_to = datetime.date.today()
        self.date_from = self.date_to - datetime.timedelta(days=30)
        self.date_to = self.date_to.strftime("%Y-%m-%d")
        self.date_from = self.date_from.strftime("%Y-%m-%d")

        # This parameter is deliberately taken big enough, so that all queries would fall into selected group.
        # Yandex Metrika API allows for such hack, returning all queries, even if they are fewer.
        self.max_results = 5000

    def __execute_query(self, query, params_q):
        params = dict(params_q)
        params['ids'] = self.client_id
        url = self.api_url + query

        http = urllib3.PoolManager()
        r = http.request(
            self.method,
            url,
            fields=params,
            headers={
                "Authorization": f"OAuth {self.token}"
            }
        )
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
        self.list_of_top_pages_dict = self.__execute_query(query=query_url, params_q=params)
        return self.list_of_top_pages_dict

    class YandexMetrikaError(Exception):
        message = None

        def __init__(self, message):
            self.message=message

        def __str__(self):
            return self.message

    def __assert(self, param, expected_type):
        try:
            assert type(param) == expected_type
        except AssertionError:
            raise self.YandexMetrikaError('Параметр неверного типа')

    def __check_page_url_for_non_empty(self, url):
        self.__assert(url, str)
        return not(url == '') and not(url[0] == '?')

    def __shorten_url(self, url):
        if url.find('?') > -1:
            return url[:url.find('?')]
        return url

    def get_unique_pages(self):
        if self.list_of_top_pages_dict is None:
            self.get_top_pages_for_period(self.date_from, self.date_to, self.max_results)

        # Sum by visits and reorder
        list_of_top_pages_with_rank = list()
        list_of_urls = list()
        l = 0
        for link in (self.list_of_top_pages_dict)['data']:
            short_url = self.__shorten_url(link['dimensions'][0]['name'])
            try:
                index = list_of_urls.index(short_url)
            except ValueError:
                list_of_urls.append(short_url)
                list_of_top_pages_with_rank.append({
                    'url': short_url,
                    'metrics': 0
                })
                index = l
                l += 1
            list_of_top_pages_with_rank[index]['metrics'] += link['metrics'][0]

        self.list_of_top_pages = sorted(list_of_top_pages_with_rank, key=lambda k: k['metrics'], reverse=True)
        self.list_of_top_pages = [d['url'] for d in self.list_of_top_pages]

        return self.list_of_top_pages

    def get_tags_by_popularity(self):
        if self.list_of_top_pages is None:
            self.get_unique_pages()
        return [
            d[d.find('/chart/tag/')+11:] for d in self.list_of_top_pages if d.find('/chart/tag/') > -1
        ]

    def get_genres_by_popularity(self):
        if self.list_of_top_pages is None:
            self.get_unique_pages()
        return [
            d[d.find('/chart/genre/') + 13:] for d in self.list_of_top_pages if d.find('/chart/genre/') > -1
        ]

    def get_studios_by_popularity(self):
        if self.list_of_top_pages is None:
            self.get_unique_pages()
        return [
            d[d.find('/chart/studio/') + 14:] for d in self.list_of_top_pages if d.find('/chart/studio/') > -1
        ]

    def get_staff_by_popularity(self):
        if self.list_of_top_pages is None:
            self.get_unique_pages()
        return [
            d[d.find('/chart/staff/') + 13:] for d in self.list_of_top_pages if d.find('/chart/staff/') > -1
        ]

    def get_novels_by_popularity(self):
        if self.list_of_top_pages is None:
            self.get_unique_pages()

        return_list = list()
        VisualNovel = apps.get_model('vn_core', 'VisualNovel')

        for url in self.list_of_top_pages:
            if url.find('/chart/') > -1:
                alias = url[url.find('/chart/') + 7:]
                if alias.find('/') == -1:
                    if alias != '' and VisualNovel.objects.filter(alias=alias).exists():
                        return_list.append(alias)

        return return_list
