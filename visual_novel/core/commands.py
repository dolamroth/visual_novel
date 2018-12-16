from django.contrib.auth.models import User

from .mixins import IsSubscribedValidator
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
