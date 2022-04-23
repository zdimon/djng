from django.urls import path, include
from .views import PageStaticView

urlpatterns = [
    path('get', PageStaticView.as_view(), name="get-static-page"),
]
