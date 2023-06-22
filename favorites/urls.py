from django.urls import path

from favorites.views import List, Toggle, Clear, AJAXToggle

app_name = 'favorites'

urlpatterns = [
    path('', List.as_view(), name='list'),
    path('<uuid:pk>/', Toggle.as_view(), name='toggle'),
    path('ajax/<uuid:pk>/', AJAXToggle.as_view(), name='ajax-toggle'),
    path('clear/', Clear.as_view(), name='clear'),
]
