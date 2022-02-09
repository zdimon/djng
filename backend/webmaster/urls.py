from django.urls import path

from .admin import webmaster_site

urlpatterns = [
    path('webmaster/', webmaster_site.urls),
]
