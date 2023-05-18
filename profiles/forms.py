from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from profiles.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'is_phone_valid'] # noqa
        field_classes = {
            'phone': PhoneNumberField,
        }
        labels = {
            "is_phone_valid": "Phone verified",
        }

    is_phone_valid = forms.BooleanField(disabled=True)


class SigninForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(self, *args, **kwargs)
        self.fields['username'].label = _('E-mail or phone')
    pass


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


class PhoneVerificationForm(forms.Form):
    secret_key = forms.CharField(max_length=10)
