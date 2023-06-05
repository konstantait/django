from django.urls import path
from currencies import views

app_name = 'currencies'

urlpatterns = [
    path('update/<str:code>', views.currency_detail, name='update'),
]
