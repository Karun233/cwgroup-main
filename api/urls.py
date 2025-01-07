"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.homepage, name=""),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', login_required(views.main_spa), name="dashboard"),

    path('api/profile/', login_required(views.profile), name='profile'),
    path('api/profile', login_required(views.profile), name='profile'),
    path('api/update-password', login_required(views.update_password), name='update_password'),
    
    path('api/hobbies/', login_required(views.user_hobbies), name="userhobbies"),
    path('api/hobbies/<int:hobby_id>/', login_required(views.delete_hobby), name="delete_hobby"),
    path('api/hobbies/add/', login_required(views.add_hobby), name="add_hobby"),
    path('api/hobbies/create/', login_required(views.create_hobby), name="create_hobby"),
    path('api/all-hobbies/', login_required(views.all_hobbies), name="all_hobbies"),
]