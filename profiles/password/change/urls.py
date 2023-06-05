from django.urls import path
from django.urls import reverse_lazy

from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
)

app_name = 'profiles.password.change'

urlpatterns = [
    path('', PasswordChangeView.as_view(
        template_name='profiles/password/change/form.html',
        success_url=reverse_lazy('profiles:password:change:done')), name='form'), # noqa
    path('done/', PasswordChangeDoneView.as_view(
        template_name='profiles/password/change/done.html'), name='done'), # noqa
]
