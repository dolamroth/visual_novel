from django.shortcuts import render, HttpResponseRedirect
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.forms import forms
from django.urls import reverse


class CaptchaForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaWidget(), label='Проверка:')


def send_offer(request, *args, **kwargs):
    form = CaptchaForm()
    if request.method == 'GET':
        return render(request, 'support/offer.html', {'form': form, **kwargs})
    elif request.method == 'POST':
        form = CaptchaForm(request.POST)
        if form.is_valid():
            offer_text = request.POST['offer_text']
            email = request.POST['email']
            return HttpResponseRedirect('/')    # redirect if success
        else:
            return HttpResponseRedirect(reverse('send_offer'))  # redirect if fail
