from django.contrib.auth.models import User

from .mixins import WeekdayValidator, IsSubscribedValidator, TimeValidator
from .models import Profile


class Command(object):
    def execute(self):
        self.validate()
        return self.execute_validated()

    def validate(self):
        """
        Override this method in subclasses to handle validation.
        """
        pass

    def execute_validated(self):
        """
        Override this method in subclass to execute command logic after validation.
        """
        pass


class ChangeUserSubsctiptionOptions(WeekdayValidator, IsSubscribedValidator, TimeValidator, Command):
    """
    :raises WrongWeekdayBitmap: Raises if "weekday" parameter is in wrong format or has incorrect value.
    :raises WrongIsSubscribed: Raises if "is_subscribed" parameter has incorrect value.
    :raises WrongTime: Raises if is "time" parameter has incorrect value.
    """

    def __init__(self, data, user):
        self.weekmap = data['weekmap']
        self.is_subscribed = data['is_subscribed']
        self.time = data['time']
        self.user = user

    def execute_validated(self):
        profile = Profile.objects.get(user=self.user)
        if self.time:
            profile.send_time = self.time
        profile.send_distributions = self.is_subscribed
        profile.weekdays = self.weekmap
        profile.save()
        print(profile.__dict__)
        # TODO: refresh subscriptions in Celery Task

    def validate(self):
        self.weekmap = self.validate_weekday_is_correct(self.weekmap)
        self.is_subscribed = self.validate_is_subscribed_field(self.is_subscribed)
        self.time = self.validate_time_field(self.time)
