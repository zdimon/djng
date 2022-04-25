from django.urls import path
from .views import LikeItView


urlpatterns = [
    path('add/', LikeItView.as_view(), name='like'),
]

