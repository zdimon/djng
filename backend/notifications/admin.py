from django.contrib import admin
from notifications.models import Notifications
from account.admin import superadmin_site

# Register your models here.
@admin.register(Notifications, site=superadmin_site)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['user', 'abonent', 'type', 'object_id', 'is_readed']