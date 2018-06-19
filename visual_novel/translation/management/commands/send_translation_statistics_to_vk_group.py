from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.urls import reverse

from notifications.vk import VK
from translation.models import (
    TranslationItemSendToVK, TranslationItem, TranslationStatisticsChapter, TranslationStatistics
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--group_id',
            type=str
        )

    def handle(self, *args, **options):
        try:
            assert options['group_id'] is not None
            # VK group ID always starts with minus sign
            assert options['group_id'][0], '-'
        except AssertionError:
            raise CommandError(
                'Формат id группы ВК в неправильном формате, требуется указать --group_id=-%group_numeric_id%')

        vk_group_id = options['group_id']

        all_translations = TranslationItem.objects.filter(
            visual_novel__is_published=True
        )

        post_flag = False
        post_text = 'Прогресс перевода визуальных новелл:\n\n'
        vk = VK()

        for translation_item in all_translations:
            translation_statistics = translation_item.statistics
            base_root = TranslationStatisticsChapter.objects.get(parent=None, lft=1,
                                                                 tree_id=translation_statistics.tree_id)

            # Zero values, if no statistics on this VN has been yet sent to this VK group
            total = 0
            translated = 0
            edited_1 = 0
            edited_2 = 0
            pictures_statistics = ''
            technical_statistics = ''
            comment = ''

            post_text_by_translation = '{}\n'.format(translation_item.visual_novel.title)
            notify_translation = False

            if TranslationItemSendToVK.objects.filter(
                    translation_item=translation_item, vk_group_id=vk_group_id
            ):
                last_statistics = TranslationItemSendToVK.objects\
                    .filter(translation_item=translation_item, vk_group_id=vk_group_id).order_by('-post_date').first()
                total = last_statistics.total_rows
                translated = last_statistics.translated
                edited_1 = last_statistics.edited_first_pass
                edited_2 = last_statistics.edited_second_pass
                pictures_statistics = last_statistics.pictures_statistics
                technical_statistics = last_statistics.technical_statistics
                comment = last_statistics.comment

            if base_root.total_rows != total:
                post_text_by_translation += 'Всего: {}\n'.format(base_root.total_rows)
                notify_translation = True

            if base_root.translated != translated:
                post_text_by_translation += 'Перевод: {}/{}\n'.format(
                    base_root.translated, base_root.total_rows
                )
                notify_translation = True

            if base_root.edited_first_pass != edited_1:
                post_text_by_translation += 'Редактура: {}/{}\n'.format(
                    base_root.edited_first_pass, base_root.total_rows
                )
                notify_translation = True

            if base_root.edited_second_pass != edited_2:
                post_text_by_translation += 'Вычитка: {}/{}\n'.format(
                    base_root.edited_second_pass, base_root.total_rows
                )
                notify_translation = True

            if translation_statistics.pictures_statistics != pictures_statistics:
                post_text_by_translation += 'Изображения: {}\n'.format(translation_statistics.pictures_statistics)
                notify_translation = True

            if translation_statistics.technical_statistics != technical_statistics:
                post_text_by_translation += 'Тех. часть: {}\n'.format(translation_statistics.technical_statistics)
                notify_translation = True

            if translation_statistics.comment != comment:
                post_text_by_translation += 'Комментарий: {}\n'.format(translation_statistics.comment)
                notify_translation = True

            post_text_by_translation += 'Страница перевода: {}\n\n'.format(
                settings.VN_HTTP_DOMAIN + translation_item.get_absolute_url()
            )

            post_flag = post_flag or notify_translation
            if notify_translation:
                post_text += post_text_by_translation
                # Save sent statistics
                TranslationItemSendToVK.objects.create_from_translation_item(translation_item, vk_group_id)

        if post_flag:
            post_text += 'Статистика предоставлена сайтом {}\nВсе переводы: {}'.format(
                settings.VN_HTTP_DOMAIN,
                settings.VN_HTTP_DOMAIN + reverse('translations_all')
            )
            vk.post_to_wall(msg=post_text, group_id=vk_group_id)
