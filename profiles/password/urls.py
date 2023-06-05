from django.urls import path, include

app_name = 'profiles.password'

urlpatterns = [
    path('change/', include('profiles.password.change.urls', namespace='change')),
    path('reset/', include('profiles.password.reset.urls', namespace='reset')),
]
