from django.urls import path

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from accounts.forms import SignupForm

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='accounts/login.html'),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', CreateView.as_view(
        template_name='accounts/signup.html',
        form_class=SignupForm,
        success_url=reverse_lazy('accounts:login')),
        name='signup'),
]
