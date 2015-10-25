from django import forms

from accounts.models import User

class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
