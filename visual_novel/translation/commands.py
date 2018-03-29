import arrow

from mptt.exceptions import InvalidMove

from core.commands import Command

from .mixins import (
    TranslationChapterExistsValidator,
    TranslationExistsValidator,
    InputNumberValidator
)
from .errors import InvalidMoveToChildElement, TranslationNotFound
from .models import TranslationStatisticsChapter


class EditTranslationChapter(
    TranslationChapterExistsValidator, TranslationExistsValidator, InputNumberValidator,
    Command
):
    """
    :raises TranslationNotFound: Raises if either translation item or translation chapter
    with respective translation item not found.
    :raises InvalidRowsQuantityInput: Raises if numbers of rows are not positive integers.
    :raises InvalidValueOnRowsQuantity: Raises if numbers of rows are inconsistent with each other.
    :raises InvalidMoveToChildElement: Raises if attempted an invalid move of chapter in chapters' tree.
    """
    def __init__(
        self, translation_item_id, translation_chapter_id, new_total, new_translated, new_edited_first_pass,
        new_edited_second_pass, new_parent, new_move_to, is_chapter, timezone
    ):
        self.translation_item_id = translation_item_id
        self.translation_chapter_id = translation_chapter_id
        self.new_total = new_total
        self.new_translated = new_translated
        self.new_edited_first_pass = new_edited_first_pass
        self.new_edited_second_pass = new_edited_second_pass
        self.new_parent = new_parent
        self.new_move_to = new_move_to
        self.is_chapter = is_chapter
        self.timezone = timezone

    def execute_validated(self):
        translation_chapter = TranslationStatisticsChapter.objects.get(id=self.translation_chapter_id)
        # TODO: pass user and add timestamp as arrow.utcnow() at user's timezone
        if not self.is_chapter:
            translation_chapter.total_rows = int(self.new_total)
            translation_chapter.translated = int(self.new_translated)
            translation_chapter.edited_first_pass = int(self.new_edited_first_pass)
            translation_chapter.edited_second_pass = int(self.new_edited_second_pass)
        translation_chapter.last_update = arrow.utcnow().to(self.timezone).datetime
        translation_chapter.save()
        if self.new_parent and self.new_move_to in ['first-child', 'last-child', 'left', 'right']:
            try:
                parent = TranslationStatisticsChapter.objects.get(
                    id=self.new_parent, tree_id=translation_chapter.tree_id
                )
                translation_chapter.move_to(parent, self.new_move_to)
                translation_chapter.save()
            except TranslationStatisticsChapter.DoesNotExist:
                raise TranslationNotFound()
            except InvalidMove:
                raise InvalidMoveToChildElement()
        return translation_chapter

    def validate(self):
        translation_item = self.validate_translation_exists(
            translation_item_id=self.translation_item_id,
        )
        self.validate_chapter_exists(
            chapter_id=self.translation_chapter_id,
            translation_item=translation_item
        )
        self.validate_numbers_input(
            total=self.new_total,
            translated=self.new_translated,
            edited_first=self.new_edited_first_pass,
            edited_second=self.new_edited_second_pass,
            is_chapter=self.is_chapter
        )
