from django.urls import path

from favorites.views import List, Add, Remove, Clear

app_name = 'favorites'

urlpatterns = [
    path('', List.as_view(), name='list'),
    path('add/<uuid:product_id>/', Add.as_view(), name='add'),
    path('remove/<uuid:product_id>/', Remove.as_view(), name='remove'),
    path('clear/', Clear.as_view(), name='clear'),

]
