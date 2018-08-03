import arrow

from mptt.exceptions import InvalidMove

from django.conf import settings
from django.template import loader
from django.urls import reverse

from core.commands import Command
from notifications.vk import VK

from .mixins import (
    TranslationChapterExistsValidator,
    TranslationExistsValidator,
    InputNumberValidator,
    ParentExistsValidator,
    BetaLinkUrlValidator,
    BetaLinkUrlUniqueValidator,
    BetaLinkExistsValidator,
    TranslationStatusExistsValidator,
    TranslationCanBeEditedValidator,
    StatusIsNotTheSameValidator
)

from .errors import InvalidMoveToChildElement, TranslationNotFound, InvalidMoveParent, CannotBeSiblingOfBaseTreeNode
from .models import TranslationStatisticsChapter, TranslationBetaLink, TranslationStatistics


class EditTranslationPartChapter(
    TranslationChapterExistsValidator, TranslationExistsValidator, TranslationCanBeEditedValidator,
    InputNumberValidator, Command
):
    """
    :raises TranslationNotFound: Raises if either translation item or translation chapter
    with respective translation item not found.
    :raises InvalidValueOnRowsQuantity: Raises if numbers of rows are inconsistent with each other.
    :raises InvalidMoveToChildElement: Raises if attempted an invalid move of chapter in chapters' tree.
    :raises InvalidMoveParent: Raises if attempted to move chapter as a child of non-section chapter.
    :raises CannotBeSiblingOfBaseTreeNode: Raises if attempted to move chapter left or right of base node.
    :raises TranslationCannotBeEditedDueToStatus: Raises if translation status does not allow editing,
    adding or deleting.
    """
    def __init__(self, data):
        self.translation_item_id = data['translation_item_id']
        self.translation_chapter_id = data['translation_chapter_id']
        self.is_chapter = True
        self.new_parent = data['new_parent']
        self.new_move_to = data['new_move_to']
        self.timezone = data['timezone']
        self.title = data['title']
        self.script_title = data['script_title']

    def modify_chapter_item_rows(self, translation_chapter):
        pass

    def execute_validated(self):
        translation_chapter = TranslationStatisticsChapter.objects.get(
            id=self.translation_chapter_id,
            is_chapter=self.is_chapter
        )

        self.modify_chapter_item_rows(translation_chapter)

        translation_chapter.title = self.title
        translation_chapter.script_title = self.script_title

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
                current_parent = translation_chapter.parent
                translation_chapter.move_to(parent, self.new_move_to)

                # Required for recalculate methods
                translation_chapter.refresh_from_db()
                parent.refresh_from_db()

                translation_chapter.save()
                translation_chapter.recalculate()
                current_parent.recalculate()
                movement = True
            except InvalidMove:
                raise InvalidMoveToChildElement()
        else:
            translation_chapter.recalculate()
        return translation_chapter, movement

    def validate(self):
        translation_item = self.validate_translation_exists(translation_item_id=self.translation_item_id)
        self.validate_translation_can_be_edited(translation_item)
        self.validate_chapter_exists(chapter_id=self.translation_chapter_id,translation_item=translation_item)


class EditTranslationChapter(EditTranslationPartChapter):
    def __init__(self, data):
        super(EditTranslationChapter, self).__init__(data)
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
        super(EditTranslationChapter, self).validate()
        self.validate_numbers_input(
            total=self.new_total,
            translated=self.new_translated,
            edited_first=self.new_edited_first_pass,
            edited_second=self.new_edited_second_pass,
            is_chapter=self.is_chapter
        )


class AddTranslationPartChapter(
    TranslationChapterExistsValidator, TranslationExistsValidator, TranslationCanBeEditedValidator,
    InputNumberValidator, ParentExistsValidator, Command
):
    """
    :raises TranslationNotFound: Raises if either translation item or translation chapter
    with respective translation item not found.
    :raises InvalidValueOnRowsQuantity: Raises if numbers of rows are inconsistent with each other.
    :raises InvalidMoveParent: Raises if attempted to move chapter as a child of non-section chapter.
    :raises CannotBeSiblingOfBaseTreeNode: Raises if attempted to move chapter left or right of base node.
    :raises TranslationCannotBeEditedDueToStatus: Raises if translation status does not allow editing,
    adding or deleting.
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
                total_rows=0,
                translated=0,
                edited_first_pass=0,
                edited_second_pass=0
            )

            translation_chapter.insert_at(
                target=self.parent,
                position=self.new_move_to,
                save=True
            )

            self.modify_chapter_item_rows(translation_chapter)
            translation_chapter.save()
            translation_chapter.recalculate()

            return translation_chapter

    def validate(self):
        self.translation_item = self.validate_translation_exists(translation_item_id=self.translation_item_id)
        self.validate_translation_can_be_edited(self.translation_item)
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
    TranslationChapterExistsValidator, TranslationExistsValidator, TranslationCanBeEditedValidator, Command
):
    """
    :raises TranslationNotFound: Raises if either translation item or translation chapter
    with respective translation item not found.
    :raises TranslationCannotBeEditedDueToStatus: Raises if translation status does not allow editing,
    adding or deleting.
    """
    def __init__(self, data):
        self.translation_item_id = data['translation_item_id']
        self.translation_chapter_id = data['translation_chapter_id']

    def execute_validated(self):
        translation_item = TranslationStatisticsChapter.objects.get(id=self.translation_chapter_id,
                                                                  tree_id=self.translation_item.statistics.tree_id)
        number_of_objects = (translation_item.rght - translation_item.lft + 1) // 2
        current_parent = translation_item.parent
        translation_item.delete()
        current_parent.recalculate()
        return number_of_objects

    def validate(self):
        self.translation_item = self.validate_translation_exists(translation_item_id=self.translation_item_id)
        self.validate_translation_can_be_edited(self.translation_item)
        self.validate_chapter_exists(chapter_id=self.translation_chapter_id, translation_item=self.translation_item)


class ManageBetaLink(
    TranslationExistsValidator, BetaLinkUrlValidator, BetaLinkUrlUniqueValidator, BetaLinkExistsValidator, Command
):
    """
    :raises TranslationNotFound: Raises if translation item not found.
    :raises InvalidBetaLinkUrl: Raises if betalink is malformed.
    :raises BetaLinkUrlAlreadyExists: Raises if another betalink with specified url already exists.
    :raises BetaLinkDoesNotExist: raises if betalink does not exist.
    """
    def __init__(self, data):
        self.translation_item_id = data['translation_item_id']
        self.title = data['title']
        self.url = data['url']
        self.comment = data['comment']
        self.betalink_id = data.get('betalink_id', 0)
        self.timezone = data['timezone']

    def execute_validated(self):
        # Additional check to reduce number of queries to database and to use PostgreSQL feature
        # to put newly saved instances at the end of filtered list when selecting
        changed = False

        # New betalink
        if self.betalink_id == 0:
            changed=True
            beta_link, _ = TranslationBetaLink.objects.get_or_create(
                title=self.title,
                url=self.url,
                comment=self.comment,
                translation_item=self.translation_item
            )
        # Already existing betalink
        else:
            beta_link = TranslationBetaLink.objects.get(id=self.betalink_id)
            if beta_link.url != self.url:
                beta_link.approved = False
                beta_link.rejected = False
                beta_link.last_update = arrow.utcnow().to(self.timezone).datetime
                changed = True
            if (beta_link.url != self.url) or (beta_link.comment != self.comment) or (beta_link.title != self.title):
                beta_link.url = self.url
                beta_link.comment = self.comment
                beta_link.title = self.title
                changed = True
            if changed:
                beta_link.save()

        if changed:
            vk = VK()
            context = {
                'link': settings.VN_HTTP_DOMAIN + reverse('admin:{}_{}_change'.format(
                            beta_link._meta.app_label,
                            beta_link._meta.model_name
                        ), args=(beta_link.pk,))
            }
            try:
                vk.send_to_user(
                    msg=loader.render_to_string('notifications/betalink_changed.txt', context),
                    user_id=settings.VK_ADMIN_LOGIN
                )
            except vk.VkError:
                pass

        return beta_link.id, beta_link.approved, beta_link.rejected

    def validate(self):
        self.translation_item = self.validate_translation_exists(translation_item_id=self.translation_item_id)
        if self.betalink_id > 0:
            self.betalink = self.validate_betalink_exists(self.betalink_id)
        self.validate_betalink_url(self.url)
        self.validate_betalink_url_unique(self.betalink_id, self.url)


class DeleteBetaLink(BetaLinkExistsValidator, Command):
    """
    :raises BetaLinkDoesNotExist: raises if betalink does not exist.
    """
    def __init__(self, data):
        self.betalink_id = data['betalink_id']

    def execute_validated(self):
        TranslationBetaLink.objects.get(id=self.betalink_id).delete(force=False)
        return 1

    def validate(self):
        self.betalink = self.validate_betalink_exists(self.betalink_id)


class ChangeTranslationStatus(TranslationExistsValidator, TranslationStatusExistsValidator,
                              StatusIsNotTheSameValidator, Command):
    """
    :raises TranslationNotFound: Raises if translation item not found.
    :raises TranslationStatusExistsValidator: raises if status with specified key does not exist.
    :raises TranslationStatusCannotBeChangedToItself: Raises if user tries to change translation status to itself.
    """

    def __init__(self, status, translation_item_id):
        self.status_key = status
        self.status_index = 0
        self.translation_item_id = translation_item_id

    def execute_validated(self):
        status = 2 ** self.status_index
        self.translation_item.status = status
        self.translation_item.save()

        # Update "last_update" for statistics
        statistics = TranslationStatistics.objects.get(id=self.translation_item.statistics.id)
        statistics.last_update = arrow.utcnow().to(settings.TIME_ZONE).datetime
        statistics.save()

    def validate(self):
        self.translation_item = self.validate_translation_exists(translation_item_id=self.translation_item_id)
        self.status_index = self.validate_translation_status_exists(self.status_key)
        self.validate_status_is_not_the_same(self.translation_item, self.status_index)
