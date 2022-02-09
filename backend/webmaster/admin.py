from django.contrib import admin
from django.contrib.admin import AdminSite

from account.mixins import DashboardRedirectMixin
from webmaster.models import Webmaster


class WebmasterAdminSite(DashboardRedirectMixin, AdminSite):
    index_title = 'Webmaster Admin Dashboard'
    site_header = 'Webmaster'


webmaster_site = WebmasterAdminSite(name='webmaster')


@admin.register(Webmaster)
class WebmasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'contact_email']
    search_fields = ['name']
