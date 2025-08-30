from rest_framework.authentication import TokenAuthentication

from vn_core.models import ExternalAPIUser


class AnonymousUser:
    @property
    def is_authenticated(self):
        return False


class SystemUser:
    @property
    def is_authenticated(self):
        return True


class ExternalAPITokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        token = ExternalAPIUser.objects.filter(is_published=True, token=key).first()
        if token is None:
            return AnonymousUser(), token
        else:
            return SystemUser(), token
