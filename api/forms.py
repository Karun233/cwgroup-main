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
                    "class": "form-control",
                    "placeholder": "YYYY-MM-DD"
                }
            ),
            'username': TextInput(attrs={"class": "form-control", "placeholder": "Enter your username"}),
            'name': TextInput(attrs={"class": "form-control", "placeholder": "Enter your name"}),
            'email': TextInput(attrs={"class": "form-control", "placeholder": "Enter your email"}),
        }
        input_formats: dict[str, list[str]] = {
            'date_of_birth': ["%Y-%m-%d"],
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


# Authenticate a user
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={"class": "form-control", "placeholder": "Enter your username"})
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password"})
    )
