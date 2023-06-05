from django import forms
from django.contrib.auth.forms import AuthenticationForm
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


class PhoneVerificationForm(forms.Form):
    secret_key = forms.CharField(max_length=10)
