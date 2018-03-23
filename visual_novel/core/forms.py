from timezone_field import TimeZoneFormField

from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CustomAuthentificationForm(AuthenticationForm):

    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    error_messages = {
        'invalid_login': _(
            "Пожалуйста, введите корректную пару имя пользователя и пароль.  "
            "Помните, что оба поля могут быть чувствительны к регистру."
        ),
        'inactive': _("Аккаунт не активен."),
    }


class CustomSignUpForm(UserCreationForm):

    error_messages = {
        'password_mismatch': _("Введённые пароли не совпадают."),
    }

    timezone = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}),
    )

    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )

    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )

    class Meta:
        model = User
        field_classes = {'username': UsernameField}
        fields = ('username', 'timezone', 'password1', 'password2',)
