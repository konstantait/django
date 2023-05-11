from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from profiles.models import User


class SigninForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(self, *args, **kwargs)
        self.fields['username'].label = _('E-mail or phone')
    pass


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('User with that email already exists')
        return email

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.username = self.cleaned_data['email'].split("@")[0]
    #     if commit:
    #         user.save()
    #     return user
