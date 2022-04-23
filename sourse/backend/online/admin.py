from django.contrib import admin
from account.admin import superadmin_site
from .models import UserOnline
# Register your models here.
@admin.register(UserOnline, site=superadmin_site)
class UserOnlineAdmin(admin.ModelAdmin):
    list_display = ['user', 'sid', 'token', 'agent', 'activity']



admin.site.register(UserOnline, UserOnlineAdmin)
