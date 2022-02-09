from django.contrib import admin
from account.admin import superadmin_site
from .models import Logserver

@admin.register(Logserver)
class LogserverAdmin(admin.ModelAdmin):
    list_display = ['server_status','url_request', 'response', 'request', 'method', 'is_ok']
