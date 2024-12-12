"""
URL configuration for test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from task_manager import views
from task_manager.user import views as login_views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('users/', include('task_manager.user.urls')),
    path('login/', login_views.UsersLoginView.as_view(), name='login'),
    path('logout/', login_views.UsersLogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('statuses/', include('task_manager.status.urls')),
    path('labels/', include('task_manager.label.urls')),
    path('tasks/', include('task_manager.task.urls')),
]