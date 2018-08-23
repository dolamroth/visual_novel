import datetime

from notifications.vk import VK
from .errors import WrongWeekdayBitmap, WrongIsSubscribed, WrongTime, WrongVkProfile


class VkProfileValidator(object):
    def check_vk_profile(self, vk_link):
        # Empty string corresponds to deleting a link
        if vk_link.__len__() == 0:
            return vk_link
        vk = VK()
        alias = vk_link[vk_link.rfind('/')+1:]
        try:
            _ = vk._get_user_id(user_alias=alias)
        except VK.VkGetUserError:
            raise WrongVkProfile
        return vk_link


class WeekdayValidator(object):
    def validate_weekday_is_correct(self, weekmap):
        try:
            weekmap = int(weekmap)
        except (TypeError, ValueError):
            raise WrongWeekdayBitmap()

        if not (0 < weekmap < 128):
            raise WrongWeekdayBitmap()

        return weekmap


class IsSubscribedValidator(object):
    def validate_is_subscribed_field(self, is_subscribed):
        if not (is_subscribed in ['true', 'false']):
            raise WrongIsSubscribed()
        return is_subscribed == 'true'


class TimeValidator(object):
    def validate_hour_field(self, hour):
        try:
            hour = int(hour)
        except ValueError:
            raise WrongTime()
        if not (0 <= hour <= 23):
            raise WrongTime()
