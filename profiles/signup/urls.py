from django.urls import path

from profiles.signup.views import (
    SignupView,
    SignupConfirmView
)

app_name = 'profiles.signup'

urlpatterns = [
    path('', SignupView.as_view(), name='form'),
    path('<uidb64>/<token>', SignupConfirmView.as_view(), name='confirm'),
]
