# forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserSignUpForm(UserCreationForm):
    # Overriding the labels for existing fields
    first_name = forms.CharField(
        required=True,
        label=_('Имя')
    )
    last_name = forms.CharField(
        required=True,
        label=_('Фамилия')
    )
    username = forms.CharField(
        required=True,
        label=_('Имя пользователя')
    )

    # Ensure password fields are translated (password1 and password2)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Пароль')}),
        label=_('Пароль'),
        required=True
    )
    password2 = forms.CharField(
        widget=
        forms.PasswordInput(attrs=
                            {'placeholder': _('Подтверждение пароля')}),
        label=_('Подтверждение пароля'),
        required=True
    )

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password1',
                  'password2')


class UserUpdateForm(UserSignUpForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.username == username:
            return username
        return super().clean_username()
