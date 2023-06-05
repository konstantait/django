from django.urls import path
from django.urls import reverse_lazy

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = 'profiles.password.reset'

urlpatterns = [
    path('', PasswordResetView.as_view(
        success_url=reverse_lazy('profiles:password:reset:done'),
        template_name='profiles/password/reset/form.html',
        email_template_name='profiles/password/reset/email.html',
        subject_template_name='profiles/password/reset/subject.txt'
    ), name='form'),
    path('done/', PasswordResetDoneView.as_view(
        template_name='profiles/password/reset/form.html',
    ), name='done'),
    path('<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('profiles:password:reset:complete'),
        template_name='profiles/password/reset/confirm.html',
    ), name='confirm'),
    path('complete/', PasswordResetCompleteView.as_view(
        template_name='profiles/password/reset/complete.html',
    ), name='complete'),
]
