import json
import logging
import urllib3
from datetime import timedelta, datetime

from django.conf import settings

__version__ = '0.1'

VK_API_VERSION = '5.131'

vk_logger = logging.getLogger('vk_logger')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VK:
    def __init__(self,api_key=settings.VK_API_KEY, api_key_messages=settings.VK_API_KEY_MESSAGES):
        self.api_key = api_key
        self.api_url = 'https://api.vk.com/method/'
        self.METHOD = 'POST'
        self.api_key_messages = api_key_messages

    def _execute_query(self, method, params_q):
        params = dict(params_q)
        params['access_token'] = self.api_key_messages if method.find('message')>-1 else self.api_key
        params['v'] = VK_API_VERSION
        url = self.api_url + method

        http = urllib3.PoolManager()
        r = http.request(self.METHOD, url, fields=params)
        try:
            return json.loads(r.data)
        except json.decoder.JSONDecodeError:
            vk_logger.error('VK API returned {}'.format(r.data))

    # TODO: authorization check inside __query() & raising corresponding exceptions
    def _query(self, method, params_q):
        return self._execute_query(method, params_q)

    def _get_user_id(self, user_alias=''):
        try:
            return (self._query('users.get', {'user_ids': user_alias}))['response'][0]['id']
        except (IndexError, KeyError):
            raise self.VkGetUserError()

    def _assert(self, param, type):
        try:
            assert type(param), type
        except AssertionError:
            raise self.VkWrongTypeError()

    def send_to_user(self, msg='', user_id=None):
        self._assert(msg, str)
        self._assert(user_id, str)
        user_id = str(self._get_user_id(user_alias=user_id.strip()))
        context = {
            'user_id': user_id,
            'message': msg,
            'random_id': 0,
        }
        r = self._query('messages.send', context)
        vk_logger.info('Message id {}'.format(r['response']))
        return r['response']

    def post_to_wall(self, msg='', group_id=settings.VK_GROUP_ID, attachments=None, close_comments=0):
        publish_date = str((datetime.now() + timedelta(days=3)).timestamp())
        self._assert(msg, str)
        self._assert(group_id, str)
        context = {
            'owner_id': group_id,
            'publish_date': publish_date,
            'message': msg,
            'friends_only': 0,
            'from_group': 1,
            'close_comments': close_comments
        }
        if attachments is not None:
            self._assert(attachments, str)
            context['attachments'] = attachments
        r = self._query('wall.post', context)
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
