from rest_framework.exceptions import APIException


class Conflict(APIException):
    status_code = 409
    default_detail = 'Conflict'
    default_code = 'conflict'

    def __init__(self, detail=None, code=None, serializer_class=None):
        super(Conflict, self).__init__(detail=detail, code=code)
        if detail is not None and serializer_class is not None:
            self.detail = self._get_serialized_error_detail(serializer_class, detail)

    def _get_serialized_error_detail(self, serializer_class, detail):
        assert detail is not None, 'Detail must not be None.'
        try:
            return serializer_class(detail).data
        except Exception as exc:
            return self.default_detail
