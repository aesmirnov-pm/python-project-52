from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.mixins import (DeleteErrorMixin, FeedbackMixin, HandleNoPermissionMixin, NeedAuthMixin,
                                 NeedPermitMixin)
from .forms import UserSignUpForm, UserUpdateForm


# ALL USERS page
class UsersView(ListView):
    model = get_user_model()
    template_name = 'users/users.html'
    ordering = ['id']


# CREATE USER page
class UsersCreateFormView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'users/new_user.html'
    success_message = 'Пользователь зарегистрирован'


# UPDATE USER page
class UsersUpdateView(SuccessMessageMixin, HandleNoPermissionMixin,
                      NeedAuthMixin, NeedPermitMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'users/update_user.html'
    login_url = reverse_lazy('login')
    unauthorized_url = reverse_lazy('users')
    success_url = reverse_lazy('users')
    success_message = 'Пользователь обновлен'


# DELETE USER page
class UsersDeleteView(SuccessMessageMixin, HandleNoPermissionMixin, NeedAuthMixin,
                      NeedPermitMixin, DeleteErrorMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/delete_user.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно удален'
    reject_message = 'Вы не можете удалить пользователя который привязан к задаче'


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
        required=True
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


# LOGIN USER page
class UsersLoginView(FeedbackMixin, LoginView):
    model = get_user_model()
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    template_name = 'login.html'
    next_page = reverse_lazy('home')
    success_message = 'Вы успешно вошли'
    error_message = 'Введите корректное имя пользователя и парооль.'


# LOGOUT USER page
class UsersLogoutView(LogoutView):
    next_page = reverse_lazy('home')
    success_message = 'Вы вышли'

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, self.success_message)
        return super().dispatch(request, *args, **kwargs)
