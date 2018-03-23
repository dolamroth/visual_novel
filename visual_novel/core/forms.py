from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm
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
