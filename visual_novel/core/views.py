import os

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.decorators import decorator_from_middleware

from notifications.service import send_email
from translation.models import TranslationItem

from .forms import CustomSignUpForm
from .utils import offset_to_timezone
from .tokens import account_activation_token
from .middlewares import IsAuthenticatedMiddleware, HasPermissionToEditProfile


def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            zone_offset = form.cleaned_data.get('timezone')
            if type(zone_offset) == int:
                user.profile.timezone = offset_to_timezone(zone_offset)
            user.save()

            current_site = get_current_site(request)
            subject = 'Активация аккаунта ' + current_site.domain
            message = render_to_string('pages/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'protocol': settings.VN_PROTOCOL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
                'token': account_activation_token.make_token(user),
            })

            user_email = form.cleaned_data.get('email')
            send_email(subject, message, user_email)

            return redirect('account_activation_sent')
    else:
        form = CustomSignUpForm()
    return render(request, 'pages/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return render(request, 'pages/account_activation_successful.html')
    else:
        return render(request, 'pages/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'pages/account_activation_sent.html')


@decorator_from_middleware(IsAuthenticatedMiddleware)
@decorator_from_middleware(HasPermissionToEditProfile)
def profile_page(request, username):
    context = dict()
    user = request.user
    context['username'] = username

    context['moderated_translations'] = list()
    moderated_translations_query = TranslationItem.objects.filter(
        visual_novel__is_published=True,
        is_published=True
    ).order_by('visual_novel__title')

    if not (user.is_superuser or user.is_staff):
        moderated_translations_query = moderated_translations_query.filter(moderators=user)

    for translation in moderated_translations_query:
        visual_novel = translation.visual_novel
        context['moderated_translations'].append({
            'title': visual_novel.title,
            'alias': visual_novel.alias
        })
    context['has_moderated_translations'] = (len(context['moderated_translations']) > 0)

    context['subscriptions'] = list()
    profile = user.profile
    for translation in profile.translationsubscription_set.all():
        visual_novel = translation.translation.visual_novel
        context['subscriptions'].append({
            'alias': visual_novel.alias,
            'title': visual_novel.title
        })
    context['has_subscriptions'] = (len(context['subscriptions']) > 0)

    weekdays = list()
    weekdays_items = profile.weekdays.items()
    weekdays_labels = profile.weekdays._labels
    ctrl_value = 1
    for i in range(len(weekdays_items)):
        weekdays.append({'name': weekdays_items[i][0], 'value': ctrl_value, 'checked': weekdays_items[i][1],
                         'label': weekdays_labels[i]})
        ctrl_value *= 2
    context['weekdays'] = weekdays
    context['distribution_time'] = profile.send_time.isoformat()[:5]
    context['distribution'] = profile.send_distributions
    context['vk_link'] = profile.vk_link

    return render(request, 'pages/profile.html', context)


def favicon(request):
    try:
        image_data = open(os.path.join(settings.BASE_DIR, "static/favicon.ico"), "rb").read()
        return HttpResponse(image_data, content_type="image/png")
    except FileNotFoundError:
        raise Http404


def google_site_verification(request, google_key):
    return render(request, 'google{}.html'.format(google_key), {})
