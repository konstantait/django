from django.urls import path

from tools.views import LoadCSV, UploadCSV

app_name = 'exchange'

urlpatterns = [
    path('load/', LoadCSV.as_view(), name='load'),
    path('upload/', UploadCSV.as_view(), name='upload'),
]
