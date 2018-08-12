from django.contrib import admin

from django.utils.html import format_html

from .models import Upload


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    fields = ('title', 'file', )
    list_display = ('get_element_display', 'title', 'watch_element')

    def get_element_display(self, obj):
        if obj.is_image():
            return format_html(
                "<img src='{}' width='100' heigth='auto' />".format(obj.get_site_url())
            )
        else:
            return obj.title
    get_element_display.short_description = ''

    def watch_element(self, obj):
        return format_html(
                "<a href='{}' target='_blank'>Смотреть файл</a>".format(obj.get_site_url())
            )
    watch_element.short_description = ''
