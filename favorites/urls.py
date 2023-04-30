from django.urls import path

from favorites import views
from favorites.views import FavoritesListView

app_name = 'favorites'

urlpatterns = [
    path('', FavoritesListView.as_view(), name='all'),
    path('add/<uuid:product_id>/', views.add, name='add'),
    path('remove/<uuid:product_id>/', views.add, name='remove'),
    path('clear/', views.clear, name='clear'),

]
