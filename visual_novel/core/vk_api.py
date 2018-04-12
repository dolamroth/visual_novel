import vk_api
from django.conf import settings


def vk_auth():
    login, password = settings.VK_LOGIN, settings.VK_PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)  # TODO to log?
        return None
    vk = vk_session.get_api()
    return vk


def post_to_group_wall(message):
    vk = vk_auth()
    if vk is None:
        return
    response = vk.wall.post(owner_id=settings.VK_GROUP_ID, from_group=1, message=message)
    return response


def post_to_user(user_id, message):
    vk = vk_auth()
    if vk is None:
        return
    response = vk.messages.send(user_id=user_id, message=message)
    return response



