from django.contrib import admin

from .models import ChartItem, ChartItemScreenshot


class ScreenshotInline(admin.TabularInline):
    model = ChartItemScreenshot
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
