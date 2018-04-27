import urllib3

from django.conf import settings

from .errors import VkAuthError, VkGetUserError

__version__ = '0.1'

# last version as of 2018-04-26, api changelog can be viewed at https://vk.com/dev/versions
VK_API_VERSION = '5.74'

# Access rights for user's token
# For more detailed info, see: https://vk.com/dev/permissions
VK_API_SCOPE=1024 + \
             4096 + \
             8192 + \
             262144 + \
             524288 + \
             1048576 + \
             4194304


class VK(object):
    def __init__(
            self,
            login=settings.VK_LOGIN,
            password=settings.VK_PASSWORD,
            api_version=VK_API_VERSION,
            scope=VK_API_SCOPE
    ):
        pass
