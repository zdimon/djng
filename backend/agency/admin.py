from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path

from .models import Agency, AgencyFiles, Agency2Woman, AgencyProfile
from account.mixins import DashboardRedirectMixin

from .mixins import AgencyFilterMixin


class AgencyAdminSite(DashboardRedirectMixin, AdminSite):
    index_title = 'Agency'
    site_header = 'Agency'


agency_site = AgencyAdminSite(name='agency')


class Agency2WomanInline(admin.TabularInline):
    model = Agency2Woman
    raw_id_fields = ('woman',)
    readonly_fields = ('admin_icon',)
    fields = ('woman', 'admin_icon')


class AgencyFilesInline(admin.StackedInline):
    '''Stacked Inline View for '''
    min_num = 3
    max_num = 20
    extra = 1
    raw_id_fields = ('agency',)
    model = AgencyFiles
    # insert_after = "name"
    fields = ('image', 'video')
    # readonly_fields = ('render_image',)


# @admin.register(Agency, site=superadmin_site)
@admin.register(Agency, site=agency_site)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'contact_email', 'director']
    search_fields = ['name']
    inlines = [AgencyFilesInline, Agency2WomanInline]
    exclude = ['password', 'username', 'last_name', 'first_name', 'user_permissions']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if hasattr(request.user, 'agencyprofile'):
            return queryset.filter(agencyprofile=request.user.agencyprofile)
        return queryset


# @admin.register(Agency2Woman, site=superadmin_site)
@admin.register(Agency2Woman, site=agency_site)
class Agency2WomanAdmin(AgencyFilterMixin, admin.ModelAdmin):
    list_display = ['agency', 'woman']
    search_fields = ['name']


# @admin.register(AgencyFiles, site=superadmin_site)
@admin.register(AgencyFiles, site=agency_site)
class AgencyFilesAdmin(AgencyFilterMixin, admin.ModelAdmin):
    list_display = ['agency', 'image', 'video']
    search_fields = ['agency']


# @admin.register(AgencyProfile, site=superadmin_site)
@admin.register(AgencyProfile, site=agency_site)
class AgencyProfileAdmin(AgencyFilterMixin, admin.ModelAdmin):
    list_display = ['agency', 'name', 'profile_type']
