from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from reviews.views import ReviewFormView

app_name = 'reviews'

urlpatterns = [
    path('', ReviewFormView.as_view(), name='create'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
