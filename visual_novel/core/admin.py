from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple

from django.contrib import admin

from translation.models import TranslationSubscription

from .models import Profile


class TranslationSubscriptionInline(admin.TabularInline):
    model = TranslationSubscription
    extra = 3


class WeekdaysFilter(admin.SimpleListFilter):
    title = 'Рассылки по дням недели'
    parameter_name = 'weekdays'

    def lookups(self, request, model_admin):
        return_tuple = []
        weekdays_bitfield = [d for d in Profile._meta.fields if d.name == 'weekdays'][0]
        labels = weekdays_bitfield.labels
        k = 1
        for i in range(0, len(labels)):
            return_tuple.append((k, labels[i]))
            k *= 2
        return return_tuple

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(weekdays=self.value())
        return queryset


class ProfileAdmin(admin.ModelAdmin):
    inlines = (TranslationSubscriptionInline,)
    list_display = (
        '__str__', 'is_staff', 'is_superuser', 'email_confirmed', 'vk_link'
    )
    list_filter = (
        'user__is_staff', WeekdaysFilter
    )
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }

admin.site.register(Profile, ProfileAdmin)
