from django.urls import path

from currencies.views import Rate

app_name = 'currencies'

urlpatterns = [
    path('', Rate.as_view(), name='rate'),
]
