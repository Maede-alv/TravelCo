from django import forms
from .models import User, Profile


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "pa")

