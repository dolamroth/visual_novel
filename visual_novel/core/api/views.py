from django.utils.decorators import decorator_from_middleware

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..commands import ChangeUserSubsctiptionOptions, ChangeUserVkLinkOption
from ..middlewares import IsAuthenticatedMiddleware, HasPermissionToEditProfile
from ..errors import WrongWeekdayBitmap, WrongIsSubscribed, WrongTime, WrongVkProfile


@api_view(['GET', 'POST', ])
@decorator_from_middleware(IsAuthenticatedMiddleware)
@decorator_from_middleware(HasPermissionToEditProfile)
def update_subscription_time(request, username):
    data = {
        'weekmap': request.GET.get('weekmap', '127'),
        'is_subscribed': request.GET.get('is_subscribed', 'false'),
        'hour': request.GET.get('hour', ''),
        'vk_link': request.GET.get('vk_link', '')
    }

    try:
        ChangeUserSubsctiptionOptions(data, request.user).execute()
        ChangeUserVkLinkOption(data, request.user).execute()
    except(WrongWeekdayBitmap, WrongIsSubscribed, WrongTime, WrongVkProfile) as exc:
        Response(data={'message': exc.message}, status=422)

    return Response(data={
        'message': 'Операция проведена успешно.'
    }, status=200)
