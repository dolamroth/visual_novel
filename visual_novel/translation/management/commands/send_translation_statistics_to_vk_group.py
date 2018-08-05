import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.urls import reverse

from notifications.vk import VK

from ...choices import TRANSLATION_ITEMS_STATUSES
from ...models import (
    TranslationItemSendToVK, TranslationItem, TranslationStatisticsChapter, TranslationBetaLinkSendToVK,
    TranslationBetaLink, TRANSLATION_ITEM_ACTIVE_BITCODE
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--group_id',
            type=str
        )

    def handle(self, *args, **options):

        translation_betalinks_sent = list()
        translation_items_sent = list()

        try:
            assert options['group_id'] is not None
            # VK group ID always starts with minus sign
            assert options['group_id'][0], '-'
        except AssertionError:
            raise CommandError(
                'Формат id группы ВК в неправильном формате, требуется указать --group_id=-%group_numeric_id%')

        vk_group_id = options['group_id']

        # Order visual novels by popularity (descending), due to peculiarities of posting to VK
        # (long posts become partially hidden)
        all_translations = TranslationItem.objects.filter(
            visual_novel__is_published=True
        ).order_by('-visual_novel__popularity')

        post_flag = False
        post_text = 'Прогресс перевода визуальных новелл:\n'
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
            status = TRANSLATION_ITEM_ACTIVE_BITCODE

            visual_novel = translation_item.visual_novel

            post_text_by_translation = '\n{} – {}\n'.format(
                visual_novel.title,
                'https://vndb.org/v' + str(visual_novel.vndb_id)
            )
            notify_translation = False

            if TranslationItemSendToVK.objects.filter(
                    translation_item=translation_item, vk_group_id=vk_group_id
            ).count():
                last_statistics = TranslationItemSendToVK.objects\
                    .filter(translation_item=translation_item, vk_group_id=vk_group_id).order_by('-post_date').first()
                total = last_statistics.total_rows
                translated = last_statistics.translated
                edited_1 = last_statistics.edited_first_pass
                edited_2 = last_statistics.edited_second_pass
                pictures_statistics = last_statistics.pictures_statistics
                technical_statistics = last_statistics.technical_statistics
                comment = last_statistics.comment
                status = last_statistics.status

            if translation_item.status.mask != status:
                bitfield_key = [d for d in translation_item.status.items() if d[1]][0][0]
                status_expanded = [d for d in TRANSLATION_ITEMS_STATUSES if d[0] == bitfield_key][0]
                if status_expanded[4]:
                    post_text_by_translation += 'Статус перевода: {}\n'.format(status_expanded[1])
                    notify_translation = True

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

            # Links on beta patches
            sent_betalinks = TranslationBetaLinkSendToVK.objects.filter(
                link__translation_item=translation_item,
                vk_group_id=vk_group_id
            )
            sent_betalinks_ids = sent_betalinks.values_list('id', flat=True)
            last_date = None
            if len(sent_betalinks) > 0:
                last_date = sent_betalinks.order_by('-post_date')[0].post_date
            betalinks = TranslationBetaLink.objects.filter(
                translation_item=translation_item,
                approved=True,
                rejected=False,
                is_published=True
            ).exclude(id__in=sent_betalinks_ids)
            if last_date:
                betalinks = betalinks.filter(last_update__gte=last_date)
            if len(betalinks):
                notify_translation = True
                for betalink in betalinks:
                    post_text_by_translation += '{} -- {}\n'.format(
                        betalink.title,
                        betalink.url
                    )
                    translation_betalinks_sent.append(
                        TranslationBetaLinkSendToVK(
                            link=betalink,
                            vk_group_id=vk_group_id,
                            post_date=datetime.date.today()
                        )
                    )

            # Translators
            translator = translation_item.translator

            if translator:
                post_text_by_translation += 'Переводчики: {}{}\n'.format(
                    translator.title,
                    '' if not translator.url else ' – {}'.format(translator.url)
                )

            post_flag = post_flag or notify_translation
            if notify_translation:
                post_text += post_text_by_translation
                # Save sent statistics
                translation_items_sent.append(
                    TranslationItemSendToVK.create_from_translation_item(translation_item, vk_group_id)
                )

        if post_flag:
            post_text += '\nСтатистика предоставлена сайтом {}\nВсе переводы: {}'.format(
                settings.VN_HTTP_DOMAIN,
                settings.VN_HTTP_DOMAIN + reverse('translations_all')
            )
            vk.post_to_wall(msg=post_text, group_id=vk_group_id)

            # If no errors, save records of sent statistics
            TranslationItemSendToVK.objects.bulk_create(translation_items_sent)
            TranslationBetaLinkSendToVK.objects.bulk_create(translation_betalinks_sent)
