from django.urls import path

from .admin import agency_site

urlpatterns = [
    path('', agency_site.urls)
]
