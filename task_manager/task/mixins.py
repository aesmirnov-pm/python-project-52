from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy


class TaskDeletionPermitMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = 'Задачу может удалить только ее автор'
        self.redirect_url = reverse_lazy('tasks')
        return super().dispatch(request, *args, **kwargs)
