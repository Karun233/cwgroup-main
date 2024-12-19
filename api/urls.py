from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from . import views  # Import the entire views module

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Dashboard / SPA Entry Point
    path('dashboard', views.main_spa, name='dashboard'),

    # Profile and Account Management
    path('profile', views.user_profile, name='profile'),
    path('change_password', views.change_password, name='change_password'),

    # Hobbies Endpoints
    path('user_hobbies', views.retrieve_user_hobbies, name='user_hobbies'),
    path('all_hobbies', views.list_all_hobbies, name='all_hobbies'),
    path('hobbies/create', views.create_new_hobby, name='create_hobby'),
    path('hobbies/add', views.add_user_hobby, name='add_hobby'),
    path('hobbies/delete/<int:hobby_id>', views.remove_user_hobby, name='delete_hobby'),
]
