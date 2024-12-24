from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'date_joined')
    search_fields = ['username', 'first_name', 'last_name', 'date_joined']
    list_filter = (('date_joined', admin.DateFieldListFilter),)
