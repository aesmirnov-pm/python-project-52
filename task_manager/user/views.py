from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.mixins import (DeleteErrorMixin, FeedbackMixin, HandleNoPermissionMixin, NeedAuthMixin,
                                 NeedPermitMixin)
from .forms import UserSignUpForm, UserUpdateForm
from .models import User


# ALL USERS page
class UsersView(ListView):
    model = User
    template_name = 'users/users.html'
    ordering = ['id']


# CREATE USER page
class UsersCreateFormView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'users/new_user.html'
    success_message = 'Пользователь зарегистрирован'


# UPDATE USER page
class UsersUpdateView(SuccessMessageMixin, HandleNoPermissionMixin,
                      NeedAuthMixin, NeedPermitMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update_user.html'
    login_url = reverse_lazy('login')
    unauthorized_url = reverse_lazy('users')
    success_url = reverse_lazy('users')
    success_message = 'Пользователь обновлен'


# DELETE USER page
class UsersDeleteView(SuccessMessageMixin, HandleNoPermissionMixin, NeedAuthMixin,
                      NeedPermitMixin, DeleteErrorMixin, DeleteView):
    model = User
    template_name = 'users/delete_user.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно удален'
    reject_message = 'Вы не можете удалить пользователя который привязан к задаче'


# LOGIN USER page
class UsersLoginView(FeedbackMixin, LoginView):
    model = User
    form_class = AuthenticationForm
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
