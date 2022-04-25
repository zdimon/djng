from django.contrib import admin
from likes.models import Likes
from account.admin import superadmin_site
# Register your models here.

@admin.register(Likes, site=superadmin_site)
class LikesAdmin(admin.ModelAdmin):
    list_display = ['liker', 'created_at', 'object_id']