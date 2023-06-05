from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import FormView, RedirectView

from profiles.signup.forms import SignupForm
from profiles.services import user_activated_by_token
from profiles.tasks import send_signup_email


class SignupView(FormView):
    template_name = 'profiles/signup/form.html'
    form_class = SignupForm
    success_url = reverse_lazy('catalog:home')
    email_template_name = 'profiles/signup/email.html'

    def form_valid(self, form):
        user = form.save()
        send_signup_email.delay(self.request, user)
        messages.success(self.request,'We will send email with registration link. Please follow link and continue your registration flow.') # noqa
        return super().form_valid(form)


class SignupConfirmView(RedirectView):
    url = reverse_lazy('profiles:login')

    def dispatch(self, *args, **kwargs):
        if 'uidb64' not in kwargs or 'token' not in kwargs:
            raise ImproperlyConfigured("The URL path must contain 'uidb64' and 'token' parameters.") # noqa
        if not user_activated_by_token(kwargs['uidb64'], kwargs['token']):
            raise Http404
        return super().dispatch(*args, **kwargs)
