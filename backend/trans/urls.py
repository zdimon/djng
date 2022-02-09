from django.urls import path, include
from .views import *
from rest_framework import routers
from .views import TransView


urlpatterns = [
    path('<str:lang>.json', TransView.as_view(), name="get-translation"),
]
