from django.urls import path
from . import views_auth

urlpatterns = [
    path('login/', views_auth.login_view, name='login_view'),
]
