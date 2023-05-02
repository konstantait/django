from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from tools.views import LoadCSV, UploadCSV

app_name = 'exchange'

urlpatterns = [
    path('load/', LoadCSV.as_view(), name='load'),
    path('upload/', UploadCSV.as_view(), name='upload'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
