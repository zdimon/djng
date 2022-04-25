from django.urls import path, include
from .views import *
from rest_framework import routers
from .views import GoogleView



urlpatterns = [
    path('google/', GoogleView.as_view(), name="auth-from-google"),
    
]
