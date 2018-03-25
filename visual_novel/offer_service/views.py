from django.shortcuts import render, HttpResponseRedirect
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.forms import forms
from django.utils.translation import gettext_lazy as _

from .models import Offer


class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(
        widget=ReCaptchaWidget(),
        label='Проверка',
        error_messages={
            'required': _('Обязательное поле.'),
        }
    )


def send_offer(request, *args, **kwargs):
    form = CaptchaForm()
    if request.method == 'GET':
        return render(request, 'support/offer.html', {'form': form, **kwargs})
    elif request.method == 'POST':
        form = CaptchaForm(request.POST)
        if form.is_valid():
            offer_text = request.POST['offer_text']
            email = request.user.email
            offer = Offer.objects.create(email=email, offer=offer_text)
            return HttpResponseRedirect('/') # redirect if success
        else:
            return render(request, 'support/offer.html', {'form': form, **kwargs}) # redirect if fail

