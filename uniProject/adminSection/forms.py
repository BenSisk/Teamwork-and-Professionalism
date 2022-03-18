from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AppUser
from django.db import transaction


class UserLoginForm(AuthenticationForm):
    def init(self, args, **kwargs):
        super(UserLoginForm, self).init(args, **kwargs)

    username = forms.TextInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '', 'id': 'hi'}))
