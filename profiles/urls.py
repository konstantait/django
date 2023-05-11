from django.urls import path

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from profiles.forms import SigninForm, SignupForm

app_name = 'profiles'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='profiles/login.html',
        form_class=SigninForm),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', CreateView.as_view(
        template_name='profiles/signup.html',
        form_class=SignupForm,
        success_url=reverse_lazy('profiles:login')),
        name='signup'),
]
