from bitfield import BitField

from django.contrib import admin

from .models import TranslationItem, TranslationBetaLink, TranslationItemSendToVK
from .widgets import StatusBitFieldWidget


class TranslationBetaLinkInline(admin.TabularInline):
    model = TranslationBetaLink
    extra = 3

    def get_queryset(self, request):
        qs = super(TranslationBetaLinkInline, self).get_queryset(request)
        return qs.filter(is_published=True)


class StatusFilter(admin.SimpleListFilter):
    title = 'Статус перевода'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return_tuple = []
        status_bitfield = [d for d in TranslationItem._meta.fields if d.name == 'status'][0]
        labels = status_bitfield.labels
        k = 1
        for i in range(0, len(labels)):
            return_tuple.append((k, labels[i]))
            k *= 2
        return return_tuple

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class TranslationItemAdmin(admin.ModelAdmin):
    inlines = (TranslationBetaLinkInline,)
    list_display = (
        '__str__', 'is_published', 'visual_novel', 'translation_status'
    )
    fields = (
        'is_published', 'moderators', 'translator', 'status', 'statistics', 'visual_novel'
    )
    formfield_overrides = {
        BitField: {'widget': StatusBitFieldWidget},
    }
    readonly_fields = ('statistics',)
    list_filter = (StatusFilter, )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('visual_novel',)
        return self.readonly_fields

    def translation_status(self, obj):
        try:
            bitfield_value = [d for d in obj.status.items() if d[1]][0]
            status = obj.status.get_label(bitfield_value[0])
        except KeyError:
            status = 'Неизвестно'
        return status
    translation_status.short_description = 'Статус'


admin.site.register(TranslationItem, TranslationItemAdmin)
admin.site.register(TranslationBetaLink)
admin.site.register(TranslationItemSendToVK)
