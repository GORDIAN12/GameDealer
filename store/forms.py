from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.Charfield()
    password=forms.Charfield(widget=forms.PasswordInput)
