import datetime

from notifications.vk import VK
from .errors import WrongWeekdayBitmap, WrongIsSubscribed, WrongTime, WrongVkProfile


class IsSubscribedValidator(object):
    def validate_is_subscribed_field(self, is_subscribed):
        if not (is_subscribed in ['true', 'false']):
            raise WrongIsSubscribed()
        return is_subscribed == 'true'
