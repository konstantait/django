from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from reviews.views import ReviewList, ReviewCreate

app_name = 'reviews'

urlpatterns = [
    path('', ReviewList.as_view(), name='list'),
    path('create', ReviewCreate.as_view(), name='create'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
