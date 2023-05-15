from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from profiles.forms import SigninForm
from profiles.views import SignupView, PhoneVerificationView, ProfileUpdateView

app_name = 'profiles'

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='profiles/login.html',
        form_class=SigninForm),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('verification/', PhoneVerificationView.as_view(), name='verification'), # noqa
    path('<int:pk>/update/', ProfileUpdateView.as_view(), name='update'),
]
