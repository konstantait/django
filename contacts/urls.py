from django.urls import path

from contacts.views import ContactView

app_name = 'contacts'

urlpatterns = [
    path('', ContactView.as_view(), name='send'),
]
