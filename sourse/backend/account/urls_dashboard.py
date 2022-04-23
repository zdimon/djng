from django.urls import path

from .admin import superadmin_site

urlpatterns = [
    path('', superadmin_site.urls)
]
