from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import News


class SuperAuthorsFilter(admin.SimpleListFilter):
    title = 'Авторы'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        return_tuple = []
        all_authors_super = User.objects.filter(is_superuser=True)
        for obj in all_authors_super:
            return_tuple.append((obj.pk, obj.username))
        return return_tuple

    def queryset(self, request, queryset):
        if self.value():
            supuser = queryset.filter(author=self.value())
            return queryset if supuser.__len__() == 0 else supuser
        return queryset


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    def poster_tag(self, obj):
        return format_html('<img src="%s" width="200" height="auto" />' % obj.poster.url if obj.poster else '')
    poster_tag.short_description = 'Постер'
    poster_tag.allow_tags = True

    def author_name(self, obj):
        if obj.author:
            return obj.author.username
        else:
            return ''
    author_name.short_description = 'Автор'

    date_hierarchy = 'created_at'
    list_filter = ['is_published', SuperAuthorsFilter]
    list_display = ('is_published', 'title', 'author_name', 'poster_tag')
    fields = ('is_published', 'author', 'title', 'alias', ('poster', 'poster_tag'), 'short_description', 'description')
    readonly_fields = ['poster_tag', 'author_name']
