import json
import logging
import urllib3

from django.conf import settings

__version__ = '0.1'

# last version as of 2018-04-26, api changelog can be viewed at https://vk.com/dev/versions
VK_API_VERSION = '5.78'

vk_logger = logging.getLogger('vk_logger')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VK(object):
    def __init__(self,api_key=settings.VK_API_KEY):
        self.api_key = api_key
        self.api_url = 'https://api.vk.com/method/'
        self.METHOD = 'GET'

    def __execute_query(self, method, params_q):
        params = dict(params_q)
        params['access_token'] = self.api_key
        params['v'] = VK_API_VERSION
        url = self.api_url + method

        http = urllib3.PoolManager()
        r = http.request(self.METHOD, url, fields=params)
        try:
            return json.loads(r.data)
        except json.decoder.JSONDecodeError:
            vk_logger.error('VK API returned {}'.format(r.data))

    # TODO: authorization check inside __query() & raising corresponding exceptions
    def __query(self, method, params_q):
        return self.__execute_query(method, params_q)

    def _get_user_id(self, user_alias=''):
        try:
            return (self.__query('users.get', {'user_ids': user_alias}))['response'][0]['id']
        except IndexError:
            raise self.VkGetUserError()

    def __assert(self, param, type):
        try:
            assert type(param), type
        except AssertionError:
            raise self.VkWrongTypeError()

    def send_to_user(self, msg='', user_id=None):
        self.__assert(msg, str)
        self.__assert(user_id, str)
        user_id = str(self._get_user_id(user_alias=user_id.strip()))
        context = {
            'user_id': user_id,
            'message': msg
        }
        r = self.__query('messages.send', context)
        vk_logger.info('Message id {}'.format(r['response']))
        return r['response']

    def post_to_wall(self, msg='', group_id=settings.VK_GROUP_ID):
        self.__assert(msg, str)
        self.__assert(group_id, str)
        context = {
            'owner_id': group_id,
            'message': msg,
            'friends_only': 0,
            'from_group': 1
        }
        r = self.__query('wall.post', context)
        vk_logger.info('Wall Post id {}'.format(r['response']))
        return r['response']

    class VkError(Exception):
        message = ''

        def __str__(self):
            return self.message

    class VkAuthError(VkError):
        message = 'Неверный логин или пароль.'

    class VkGetUserError(VkError):
        message = 'Такого пользователя не существует.'

    class VkNoReceiverError(VkError):
        message = 'Требуется указать параметр user_id, либо user_ids.'

    class VkWrongTypeError(VkError):
        message = 'Переданный параметр неправильного типа.'
