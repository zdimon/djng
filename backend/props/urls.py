from django.urls import path, include
from .views import *
from rest_framework import routers
from .views import PropsListView, PropsSaveView



urlpatterns = [
    path('list/<str:gender>', PropsListView.as_view(), name="props-list"),
    path('save/', PropsSaveView.as_view(), name="props-save")
]
