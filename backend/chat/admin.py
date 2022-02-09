from django.contrib import admin
from account.admin import superadmin_site
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
# Register your models here.

from .models import ChatMessage, ChatRoom, ChatContact

@admin.register(ChatRoom, site=superadmin_site)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'is_active', 'is_answered', 'is_low_account', 'is_video', 'activity']
    list_filter = ['is_active', 'is_answered']
admin.site.register(ChatRoom, ChatRoomAdmin)

class ChatContactAdmin(admin.ModelAdmin):
    list_display = ['room', 'owner', 'abonent', 'is_current', 'is_camera', 'created_at']
admin.site.register(ChatContact, ChatContactAdmin)

@admin.register(ChatMessage, site=superadmin_site)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'message', 'is_readed', 'is_private', 'related_object_link']

    def related_object_link(self, obj):
        try:
            url = obj.content_object.get_admin_url
            return mark_safe('<a class="grp-button" href="{0}">{1}</a>'.format(url, _('Связанный объект')))
        except:
            return 'None'
admin.site.register(ChatMessage, ChatMessageAdmin)