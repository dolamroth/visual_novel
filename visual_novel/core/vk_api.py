import vk_api

from django.conf import settings


class VkError(Exception):
    message = ''
    def __str__(self):
        assert self.message is not None, ('Неизвестная ошибка.')
        return self.message


class VkAuthError(VkError):
    message = 'Неверный логин или пароль.'


class VkGetUserError(VkError):
    message = 'Такого пользователя не существует.'


def vk_auth():
    login, password = settings.VK_LOGIN, settings.VK_PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError:
        raise VkAuthError()
    vk = vk_session.get_api()
    return vk


def post_to_group_wall(message):
    vk = vk_auth()
    response = vk.wall.post(owner_id=settings.VK_GROUP_ID, from_group=1, message=message)
    return response


def post_to_user(user_id, message):
    vk = vk_auth()
    response = vk.messages.send(user_id=get_user_id_by_alias(user_id), message=message)
    return response


def get_user_id_by_alias(user_alias):
    vk = vk_auth()
    try:
        response = vk.users.get(user_ids=user_alias)
    except vk_api.exceptions.ApiError:
        raise VkGetUserError()
    return response[0]['id']
