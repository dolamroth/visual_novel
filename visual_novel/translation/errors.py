class TranslationError(Exception):

    message = ''

    def __str__(self):
        assert self.message is not None, (
            'Неизвестная ошибка.'
        )
        return self.message


class TranslationNotFound(TranslationError):
    message = 'Глава или статистика перевода не найдена.'


class InvalidMoveToChildElement(TranslationError):
    message = 'Нельзя переместить главу или раздел внутрь самого себя.'


class InvalidRowsQuantityInput(TranslationError):
    message = 'Число строк должно быть положительным целым числом.'


class InvalidValueOnRowsQuantity(TranslationError):
    message = 'Некорректное соотношение между числом строк (всего, переведено, отредактировано).'
