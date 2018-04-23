from django.utils.decorators import decorator_from_middleware

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..commands import ChangeUserSubsctiptionOptions
from ..middlewares import IsAuthenticatedMiddleware, HasPermissionToEditProfile
from ..errors import WrongWeekdayBitmap, WrongIsSubscribed, WrongTime


@api_view(['GET', 'POST', ])
@decorator_from_middleware(IsAuthenticatedMiddleware)
@decorator_from_middleware(HasPermissionToEditProfile)
def update_subscription_time(request, username):

    data = {
        'weekmap': request.GET.get('weekmap', '127'),
        'is_subscribed': request.GET.get('is_subscribed', 'false'),
        'time': request.GET.get('time', ''),
    }

    try:
        ChangeUserSubsctiptionOptions(data, request.user).execute()
    except(WrongWeekdayBitmap, WrongIsSubscribed, WrongTime) as exc:
        Response(data={'message': exc.message}, status=422)

    return Response(data={
        'message': 'Операция проведена успешно.'
    }, status=200)
