from rest_framework import serializers
from translation.choices import TRANSLATION_ITEMS_STATUSES
from rest_framework_recursive.fields import RecursiveField
from drf_yasg.utils import swagger_serializer_method
from django.urls import reverse
from django.conf import settings


def nested_set_to_tree(items):
    items = sorted(items, key=lambda x: x['lft'])
    stack = []
    root = []
    for item in items:
        item['children'] = []
        while stack and stack[-1]['rght'] < item['lft']:
            stack.pop()
        if stack:
            stack[-1]['children'].append(item)
        else:
            root.append(item)
        stack.append(item)
    return root


class TranslationItemVisualNovelResponseSerializer(serializers.Serializer):
    title = serializers.CharField()
    alternative_title = serializers.CharField()
    vndb_id = serializers.IntegerField()
    rate = serializers.IntegerField()
    vote_count = serializers.IntegerField()
    alias = serializers.CharField()


class TranslationItemTranslatorResponseSerializer(serializers.Serializer):
    title = serializers.CharField()
    url = serializers.CharField()


class TranslationItemTranslationChapterResponseSerializer(serializers.Serializer):
    title = serializers.CharField()
    script_title = serializers.CharField()
    id = serializers.IntegerField()
    parent_id = serializers.IntegerField(allow_null=True)
    last_update = serializers.DateTimeField()
    level = serializers.IntegerField()
    left_key = serializers.IntegerField(source="lft", help_text="Левый ключ в модели Nested Sets")
    right_key = serializers.IntegerField(source="rght", help_text="Правый ключ в модели Nested Sets")
    is_chapter = serializers.BooleanField()
    total_rows = serializers.IntegerField()
    translated = serializers.IntegerField()
    edited_first_pass = serializers.IntegerField()
    edited_second_pass = serializers.IntegerField()


class TranslationItemResponseSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()
    visual_novel = TranslationItemVisualNovelResponseSerializer()
    translator = TranslationItemTranslatorResponseSerializer()
    items = TranslationItemTranslationChapterResponseSerializer(many=True)
    page_on_site = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.ChoiceField(choices=[item[:2] for item in TRANSLATION_ITEMS_STATUSES]))
    def get_status(self, obj):
        for key, value in obj.status.items():
            if value is True:
                return key

    @swagger_serializer_method(serializer_or_field=serializers.URLField())
    def get_page_on_site(self, obj):
        return settings.VN_HTTP_DOMAIN + reverse('translation_item', kwargs={'vn_alias': obj.visual_novel.alias})


class TranslationItemTranslationChapterNestedResponseSerializer(TranslationItemTranslationChapterResponseSerializer):
    children = serializers.ListSerializer(
        child=RecursiveField("TranslationItemTranslationChapterNestedResponseSerializer")
    )


class TranslationItemNestedResponseSerializer(TranslationItemResponseSerializer):
    items = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=TranslationItemTranslationChapterNestedResponseSerializer)
    def get_items(self, obj):
        if obj.items:
            return nested_set_to_tree(obj.items)[0]
