from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from bitfield.admin import BitFieldListFilter

from django.contrib import admin

from translation.models import TranslationSubscription

from .models import Profile


class TranslationSubscriptionInline(admin.TabularInline):
    model = TranslationSubscription
    extra = 3


class ProfileAdmin(admin.ModelAdmin):
    inlines = (TranslationSubscriptionInline,)
    list_display = (
        '__str__', 'is_staff', 'is_superuser', 'email_confirmed'
    )
    list_filter = (
        'user__is_staff', ('weekdays', BitFieldListFilter,)
    )
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }




admin.site.register(Profile, ProfileAdmin)
