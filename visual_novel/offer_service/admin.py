from django.contrib import admin
from .models import Offer
from django import forms


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('name', 'email', 'offer', 'is_considered', 'is_accepted', 'is_rejected', 'rejected_reasons')

    def clean(self):
        if 'is_considered' in self.changed_data and not self.cleaned_data.get('is_considered'):
            raise forms.ValidationError('Нельзя убирать заявку из рассмотрения')
        is_considered = self.cleaned_data.get('is_considered')
        is_accepted = self.cleaned_data.get('is_accepted')
        is_rejected = self.cleaned_data.get('is_rejected')
        if not is_considered and (is_rejected or is_accepted):
            raise forms.ValidationError("Нельзя принимать (отклонять) заявку до ее рассмотрения")
        if is_accepted and is_rejected:
            raise forms.ValidationError("Нельзя одновременно принимать и отклонять заявку")
        return self.cleaned_data


class OfferAdmin(admin.ModelAdmin):
    form = OfferForm


admin.site.register(Offer, OfferAdmin)

