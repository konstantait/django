from django.urls import path

from .views import SignupView, LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# from django.urls import path
#
# from . import views
#
# urlpatterns = [
#     path('login/', views.login, name='login'),
#     path('signup/', views.signup, name='signup'),
#     path('logout/', views.logout, name='logout'),
# ]
