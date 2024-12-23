from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from typing import Optional


# Create/Register a user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields: list[str] = ['username', 'name', 'email', 'date_of_birth', 'password1', 'password2']
        widgets: dict[str, forms.Widget] = {
            'date_of_birth': forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date", 
                    "class": "form-control"
                }
            ),
        }
        input_formats: dict[str, list[str]] = {
            'date_of_birth': ["%Y-%m-%d"],
        }


# Authenticate a user
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())