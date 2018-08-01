class ProfileError(Exception):

    message = ''

    def __str__(self):
        assert self.message is not None, (
            'Неизвестная ошибка.'
        )
        return self.message


class WrongWeekdayBitmap(ProfileError):
    message = 'Недопустимая битовая маска дней недели.'


class WrongIsSubscribed(ProfileError):
    message = 'Параметр is_subscribed должен принимать одно из значений {true, false}.'


class WrongTime(ProfileError):
    message = 'Время в недопустимом формате.'


class WrongVkProfile(ProfileError):
    message = 'Такого пользователя не существует'
