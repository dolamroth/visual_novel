from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import CustomSignUpForm
from .utils import offset_to_timezone


def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            zone_offset = form.cleaned_data.get('timezone')
            if type(zone_offset) == int:
                user.profile.timezone = offset_to_timezone(zone_offset)
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = CustomSignUpForm()
    return render(request, 'pages/signup.html', {'form': form})
