from django.contrib.auth.forms import forms, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True, label=_('Имя'))
    last_name = forms.CharField(required=True, label=_('Фамилия'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class UserUpdateForm(UserSignUpForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.username == username:
            return username
        return super().clean_username()
