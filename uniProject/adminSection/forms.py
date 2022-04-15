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

class DocumentForm(forms.Form):
    title = forms.CharField(label='Project Title', max_length=30)
    desc = forms.CharField(widget=forms.Textarea(attrs={'title': 'Project Description'}), label='Project Description', max_length=200)
    docfile = forms.FileField(label='Select a file')
