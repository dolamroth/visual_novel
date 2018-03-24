import pytz
import datetime
from itertools import chain

from django.conf import settings

ru_months_in = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
TZ_DETECT_COUNTRIES = getattr(settings, 'TZ_DETECT_COUNTRIES', ('RU', 'UA', 'BY', 'KZ'))


def printable_russian_date(date):
    return str(date.day) + ' ' + ru_months_in[date.month - 1] + ' ' + str(date.year) + ' года'


def get_prioritized_timezones():
    def tz_gen():
        for c in TZ_DETECT_COUNTRIES:
            yield pytz.country_timezones(c)
        yield pytz.common_timezones

    return chain.from_iterable(tz_gen())


# All functions copied from django-tz-detect
# https://github.com/adamcharnock/django-tz-detect
def offset_to_timezone(offset):
    """Convert a minutes offset (JavaScript-style) into a pytz timezone
    The ``now`` parameter is generally used for testing only
    """
    now = datetime.datetime.now()

    # JS offsets are flipped, so unflip.
    user_offset = -offset

    # Helper: timezone offset in minutes
    def get_tz_offset(tz):
        try:
            return tz.utcoffset(now).total_seconds() / 60
        except (pytz.NonExistentTimeError, pytz.AmbiguousTimeError):
            return tz.localize(now, is_dst=False).utcoffset().total_seconds() / 60

    # Return the timezone with the minimum difference to the user's offset.
    return min(
        (pytz.timezone(tz_name) for tz_name in get_prioritized_timezones()),
        key=lambda tz: abs(get_tz_offset(tz) - user_offset),
    )
