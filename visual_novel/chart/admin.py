from django.contrib import admin
from django.utils.html import format_html

from .models import ChartItem, ChartItemScreenshot


class ScreenshotInline(admin.TabularInline):
    def image_tag(self):
        return format_html('<img src="%s" width=200 height=150 />' % self.image.url if self.image else '')

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
    inlines = (ScreenshotInline, )
    list_display = (
        'visual_novel', 'is_published', 'date_of_translation'
    )


admin.site.register(ChartItem, ChartItemAdmin)
