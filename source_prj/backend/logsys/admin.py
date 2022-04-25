from django.contrib import admin
from logsys.models import Log

# Register your models here.
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['username','ip_address', 'user_agent', 'view_name']