from django.urls import path

from reviews.views import ReviewList, ReviewCreate

app_name = 'reviews'

urlpatterns = [
    path('', ReviewList.as_view(), name='list'),
    path('create', ReviewCreate.as_view(), name='create'),
]
