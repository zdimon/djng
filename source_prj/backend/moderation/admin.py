from django.contrib import admin, messages
from django.contrib.admin import AdminSite

from account.mixins import DashboardRedirectMixin
from .models import Moderation, ModerationFiles
from .utils.woman import manke_html_from_json
from .utils.agency import make_agency_html_from_json

from django.utils.safestring import mark_safe
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from .utils.dispacher import dispatch
# Register your models here.

from .utils.photo import show_photo
from .utils.video import show_video
from .utils.feed import show_feed
from account.admin import superadmin_site


class ModeratorAdminSite(DashboardRedirectMixin, AdminSite):
    index_title = 'Webmaster Admin Dashboard'
    site_header = 'Webmaster'


moderator_site = ModeratorAdminSite(name='admin')


class Agency2WomanInline(admin.TabularInline):
    model = ModerationFiles
    raw_id_fields = ('moderation', )



# @admin.register(Moderation, site=superadmin_site)
# @admin.register(Moderation, site=moderator_site)
@admin.register(Moderation)
class ModerationAdmin(admin.ModelAdmin):
    inlines = [ Agency2WomanInline ]
    list_display = ['name', 'type_obj', 'is_new','prop_html','approve_link','disapprove_link','related_object_link']
    list_filter = ['type_obj']
    readonly_fields = ('prop_html',)
    exclude = ('data',)
    def prop_html(self, obj):
        if obj.type_obj == 'woman-profile':
            return manke_html_from_json(obj)
        if obj.type_obj == 'agency':
            return make_agency_html_from_json(obj)
        if obj.type_obj == 'photo-new' or obj.type_obj == 'photo-delete':
            return show_photo(obj.content_object)
        if obj.type_obj == 'video-new' or obj.type_obj == 'video-delete':
            return show_video(obj.content_object)
        if obj.type_obj == 'feed-new' or obj.type_obj == 'feed-delete':
            return show_feed(obj.content_object)

    def approve_link(self, obj):
        url = 'approve/%s' % obj.id;
        
        return mark_safe('<a class="grp-button" href="{0}">{1}</a>'.format(url, _('Approve')))

    def disapprove_link(self, obj):
        url = 'disapprove/%s' % obj.id;
        
        return mark_safe('<a class="grp-button grp-delete-link" href="{0}">{1}</a>'.format(url, _('Disapprove')))

    def related_object_link(self, obj):
        try:
            url = obj.content_object.get_admin_url
            return mark_safe('<a class="grp-button" href="{0}">{1}</a>'.format(url, _('Модерируемый объект')))
        except:
            return 'None'

    def approve(self,request,id):
        messages.success(request, _('Object has been approved!'))
        dispatch(id,'approve')
        return redirect(reverse('admin:moderation_moderation_changelist'))

    def disapprove(self,request,id):
        messages.error(request, _('Object has been disapproved!'))
        dispatch(id,'disapprove')
        return redirect(reverse('admin:moderation_moderation_changelist'))

    def get_urls(self):
        urls = super(ModerationAdmin, self).get_urls()
        admin_urls = [
            path('approve/<int:id>', self.admin_site.admin_view(self.approve),name="admin-approve"),
            path('disapprove/<int:id>', self.admin_site.admin_view(self.disapprove),name="admin-disapprove")
        ]
        return admin_urls + urls
