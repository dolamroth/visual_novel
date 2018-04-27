class VkError(Exception):
    message = ''
    def __str__(self):
        assert self.message is not None, ('Неизвестная ошибка.')
        return self.message


class VkAuthError(VkError):
    message = 'Неверный логин или пароль.'


class VkGetUserError(VkError):
    message = 'Такого пользователя не существует.'
