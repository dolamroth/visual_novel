from captcha.fields import ReCaptchaField

from django.shortcuts import render, HttpResponseRedirect
from django.forms import forms
from django.utils.decorators import decorator_from_middleware

from core.middlewares import IsAuthenticatedMiddleware
from .models import Offer


class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()


@decorator_from_middleware(IsAuthenticatedMiddleware)
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
