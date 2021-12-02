from django import forms
from django.core.validators import RegexValidator
from .models import User, Post


class LogInForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
