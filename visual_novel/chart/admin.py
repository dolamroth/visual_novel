from django.contrib import admin

from .models import ChartItem, ChartItemScreenshot


class ScreenshotInline(admin.TabularInline):
    model = ChartItemScreenshot
    fields = ('is_published', 'title', 'image', 'image_tag', 'order')
    readonly_fields = ('image_tag',)
    extra = 3


class ChartItemAdmin(admin.ModelAdmin):
    inlines = (ScreenshotInline, )
    list_display = (
        'visual_novel', 'is_published', 'date_of_translation'
    )


admin.site.register(ChartItem, ChartItemAdmin)
