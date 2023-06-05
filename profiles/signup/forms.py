from django import forms
from django.contrib.auth.forms import UserCreationForm

from profiles.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('User with that email already exists')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone, is_phone_valid=True).exists():
            raise forms.ValidationError('User with that phone already exists')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user
