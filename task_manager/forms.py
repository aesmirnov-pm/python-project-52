from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class InactiveUserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Имя пользователя')
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Пароль')
            }
        )
    )

    class Meta:
        fields = ('username', 'password')

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                'Аккаунт деактивирован',
                code='inactive')
