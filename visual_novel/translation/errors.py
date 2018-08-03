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


class ParentDoesNotExist(TranslationError):
    message = 'Указанный родительский раздел не существует.'


class CannotBeSiblingOfBaseTreeNode(TranslationError):
    message = 'Главы или разделы не могут располагаться на том же уровне, что и раздел самого высокого уровня.'


class InvalidBetaLinkUrl(TranslationError):
    message = 'Невалидный URL.'


class BetaLinkUrlAlreadyExists(TranslationError):
    message = 'Ссылка с указанным URL уже существует.'


class BetaLinkDoesNotExist(TranslationError):
    message = 'Указанная ссылка не существует.'


class TranslationStatusDoesNotExist(TranslationError):
    message = 'Такого статуса перевода не существует.'


class TranslationStatusCannotBeChangedToItself(TranslationError):
    message = 'Нельзя сменить статус на тот же самый.'


class TranslationCannotBeEditedDueToStatus(TranslationError):
    message = 'Статус перевода не позволяет редактирование, добавление или удаление.'
