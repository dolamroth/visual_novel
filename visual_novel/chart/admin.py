from django.contrib import admin
from django.utils.html import format_html

from .models import ChartItem, ChartItemScreenshot, ChartItemTranslator, ChartItemToUser


class ChartItemTranslatorInline(admin.TabularInline):
    model = ChartItemTranslator
    extra = 3


class ScreenshotInline(admin.TabularInline):
    def image_tag(self, obj):
        return format_html('<img src="%s" width="150" height="auto" />' % obj.image.url if obj.image else '')

    image_tag.short_description = 'Фотография'
    image_tag.allow_tags = True
    model = ChartItemScreenshot
    fields = ('is_published', 'title', 'image', 'image_tag', 'order')
    readonly_fields = ('image_tag',)
    extra = 3

    def get_queryset(self, request):
        qs = super(ScreenshotInline, self).get_queryset(request)
        return qs.exclude(image__exact='')


class ChartItemAdmin(admin.ModelAdmin):
    inlines = (ScreenshotInline, ChartItemTranslatorInline, )
    list_display = (
        'visual_novel', 'is_published', 'date_of_translation'
    )


class ChartItemToUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('chart_item',)


admin.site.register(ChartItem, ChartItemAdmin)
admin.site.register(ChartItemToUser, ChartItemToUserAdmin)
