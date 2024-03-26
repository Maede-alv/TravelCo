from django import forms
from .models import User, Profile


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "verification_code")


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "phone")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Password's not match.")
        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("E-mail already in use.")
        return data

    def clean_phone(self):
        data = self.cleaned_data["phone"]
        if User.objects.filter(phone=data).exists():
            raise forms.ValidationError("Phone number already exist.")
        return data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name")
