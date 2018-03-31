import arrow

from mptt.exceptions import InvalidMove

from core.commands import Command

from .mixins import (
    TranslationChapterExistsValidator,
    TranslationExistsValidator,
    InputNumberValidator,
    ParentExistsValidator,
)
from .errors import InvalidMoveToChildElement, TranslationNotFound, InvalidMoveParent, CannotBeSiblingOfBaseTreeNode
from .models import TranslationStatisticsChapter


class EditTranslationPartChapter(
    TranslationChapterExistsValidator, TranslationExistsValidator, InputNumberValidator, Command
):
    """
    :raises TranslationNotFound: Raises if either translation item or translation chapter
    with respective translation item not found.
    :raises InvalidValueOnRowsQuantity: Raises if numbers of rows are inconsistent with each other.
    :raises InvalidMoveToChildElement: Raises if attempted an invalid move of chapter in chapters' tree.
    :raises InvalidMoveParent: Raises if attempted to move chapter as a child of non-section chapter.
    :raises CannotBeSiblingOfBaseTreeNode: Raises if attempted to move chapter left or right of base node.
    """
    def __init__(self, data):
        self.translation_item_id = data['translation_item_id']
        self.translation_chapter_id = data['translation_chapter_id']
        self.is_chapter = data['is_chapter']
        self.new_parent = data['new_parent']
        self.new_move_to = data['new_move_to']
        self.timezone = data['timezone']
        self.title = data['title']
        self.script_title = data['script_title']

    def modify_chapter_item_rows(self, translation_chapter):
        pass

    def execute_validated(self):
        translation_chapter = TranslationStatisticsChapter.objects.get(id=self.translation_chapter_id)

        self.modify_chapter_item_rows(translation_chapter)

        translation_chapter.title = self.title
        translation_chapter.script_title = self.script_title

        # TODO: pass user and add timestamp as arrow.utcnow() at user's timezone
        translation_chapter.last_update = arrow.utcnow().to(self.timezone).datetime
        translation_chapter.save()

        movement = False
        if self.new_parent \
                and type(self.new_parent) == int \
                and self.new_move_to in ['first-child', 'last-child', 'left', 'right']:
            # 1. Find parent node
            try:
                parent = TranslationStatisticsChapter.objects.get(
                    id=self.new_parent, tree_id=translation_chapter.tree_id
                )
            except TranslationStatisticsChapter.DoesNotExist:
                raise TranslationNotFound()
            # 2. Check that user doesn't try to move chapter as a child of non-section chapter
            if not parent.is_chapter and self.new_move_to in ['first-child', 'last-child']:
                raise InvalidMoveParent()
            # 3. Check that user doesn't try to move chapter on the same level as base tree element
            if parent.lft == 1 and self.new_move_to in ['left', 'right']:
                raise CannotBeSiblingOfBaseTreeNode()
            # 4. Make movement
            # Check that it is valid, i.e. user doesn't try to move parental node to be child of it's own child
            try:
                translation_chapter.move_to(parent, self.new_move_to)
                translation_chapter.save()
                movement = True
            except InvalidMove:
                raise InvalidMoveToChildElement()
        return translation_chapter, movement

    def validate(self):
        translation_item = self.validate_translation_exists(translation_item_id=self.translation_item_id)
        self.validate_chapter_exists(chapter_id=self.translation_chapter_id,translation_item=translation_item)


class EditTranslationChapter(EditTranslationPartChapter):
    def __init__(self, data):
        super(EditTranslationChapter, self).__init__(data)
        self.new_total = data['total']
        self.new_translated = data['new_translated']
        self.new_edited_first_pass = data['new_edited_first_pass']
        self.new_edited_second_pass = data['new_edited_second_pass']

    def modify_chapter_item_rows(self, translation_chapter):
        translation_chapter.total_rows = int(self.new_total)
        translation_chapter.translated = int(self.new_translated)
        translation_chapter.edited_first_pass = int(self.new_edited_first_pass)
        translation_chapter.edited_second_pass = int(self.new_edited_second_pass)

    def validate(self):
        super(EditTranslationChapter, self).validate()
        self.validate_numbers_input(
            total=self.new_total,
            translated=self.new_translated,
            edited_first=self.new_edited_first_pass,
            edited_second=self.new_edited_second_pass,
            is_chapter=self.is_chapter
        )


class AddTranslationPartChapter(
    TranslationChapterExistsValidator, TranslationExistsValidator, InputNumberValidator, ParentExistsValidator, Command
):
    """
    :raises TranslationNotFound: Raises if either translation item or translation chapter
    with respective translation item not found.
    :raises InvalidValueOnRowsQuantity: Raises if numbers of rows are inconsistent with each other.
    :raises InvalidMoveParent: Raises if attempted to move chapter as a child of non-section chapter.
    :raises CannotBeSiblingOfBaseTreeNode: Raises if attempted to move chapter left or right of base node.
    """
    def __init__(self, data):
        self.translation_item_id = data['translation_item_id']
        self.is_chapter = True
        self.new_parent = data['new_parent']
        self.new_move_to = data['new_move_to']
        self.timezone = data['timezone']
        self.title = data['title']
        self.script_title = data['script_title']

    def modify_chapter_item_rows(self, translation_chapter):
        pass

    def execute_validated(self):
        if not self.new_move_to in ['first-child', 'last-child', 'left', 'right']:
            self.new_move_to = 'last-child'
        if self.new_move_to in ['left', 'right'] and self.parent.lft == 1:
            raise CannotBeSiblingOfBaseTreeNode()
        else:

            translation_chapter = TranslationStatisticsChapter(
                title=self.title,
                script_title=self.script_title,
                is_chapter=self.is_chapter,
                last_update=arrow.utcnow().to(self.timezone).datetime,
            )

            translation_chapter.insert_at(
                target=self.parent,
                position=self.new_move_to,
                save=True
            )

            self.modify_chapter_item_rows(translation_chapter)
            translation_chapter.save()

            return translation_chapter

    def validate(self):
        self.translation_item = self.validate_translation_exists(translation_item_id=self.translation_item_id)
        self.parent = self.validate_parent_section_exists(self.translation_item, self.new_parent, self.new_move_to)


class AddTranslationChapter(AddTranslationPartChapter):
    def __init__(self, data):
        super(AddTranslationChapter, self).__init__(data)
        self.new_total = data['total']
        self.new_translated = data['new_translated']
        self.new_edited_first_pass = data['new_edited_first_pass']
        self.new_edited_second_pass = data['new_edited_second_pass']
        self.is_chapter = False

    def modify_chapter_item_rows(self, translation_chapter):
        translation_chapter.total_rows = int(self.new_total)
        translation_chapter.translated = int(self.new_translated)
        translation_chapter.edited_first_pass = int(self.new_edited_first_pass)
        translation_chapter.edited_second_pass = int(self.new_edited_second_pass)

    def validate(self):
        super(AddTranslationChapter, self).validate()
        self.validate_numbers_input(
            total=self.new_total,
            translated=self.new_translated,
            edited_first=self.new_edited_first_pass,
            edited_second=self.new_edited_second_pass,
            is_chapter=self.is_chapter
        )


class DeleteTranslationChapter(
    TranslationChapterExistsValidator, TranslationExistsValidator, Command
):
    """
    :raises TranslationNotFound: Raises if either translation item or translation chapter
    with respective translation item not found.
    """
    def __init__(self, data):
        self.translation_item_id = data['translation_item_id']
        self.translation_chapter_id = data['translation_chapter_id']

    def execute_validated(self):
        translation_item = TranslationStatisticsChapter.objects.get(id=self.translation_chapter_id,
                                                                  tree_id=self.translation_item.statistics.tree_id)
        number_of_objects = (translation_item.rght - translation_item.lft + 1) // 2
        translation_item.delete()
        return number_of_objects

    def validate(self):
        self.translation_item = self.validate_translation_exists(translation_item_id=self.translation_item_id)
        self.validate_chapter_exists(chapter_id=self.translation_chapter_id, translation_item=self.translation_item)
