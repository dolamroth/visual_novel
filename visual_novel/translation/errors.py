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


class InvalidValueOnRowsQuantity(TranslationError):
    message = 'Некорректное соотношение между числом строк (всего, переведено, отредактировано).'


class InvalidMoveParent(TranslationError):
    message = 'Глава (не раздел) не может быть родительским элементом для другой главы или раздела.'
