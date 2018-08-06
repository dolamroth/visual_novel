from django import forms
from django.template import loader
from django.contrib.auth.forms import (
    UsernameField, AuthenticationForm, UserCreationForm, PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from notifications.service import send_email
from .validators import validate_vk_profile


class CustomAuthentificationForm(AuthenticationForm):

    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )

    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    error_messages = {
        'invalid_login': _(
            "Пожалуйста, введите корректную пару имя пользователя и пароль."
            "Помните, что оба поля могут быть чувствительны к регистру."
        ),
        'inactive': _("Аккаунт не активен."),
    }


class CustomSignUpForm(UserCreationForm):

    timezone = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}),
    )

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}),
    )

    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
    )

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )

    vk_account = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "required": False, "placeholder": "https://vk.com/id1"}),
        strip=False,
        max_length=254,
        validators=[validate_vk_profile],
        required=False
    )

    class Meta:
        model = User
        field_classes = {'username': UsernameField}
        fields = ('username', 'timezone', 'email', 'password1', 'password2', 'vk_account')


class CustomPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}),
    )

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        message = loader.render_to_string(email_template_name, context)

        send_email(subject, message, to_email)


class CustomSetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )

    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
