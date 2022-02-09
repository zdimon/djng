from django.contrib import admin
from image_cropping import ImageCroppingMixin
from account.admin import superadmin_site

# Register your models here.
from account.admin import superadmin_site
from .models import UserMedia
# Register your models here.

@admin.register(UserMedia)
class UserMediaAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_editable = ('is_approved',)
    list_filter = ['is_approved', 'is_deleted', 'type_media', 'role_media', 'orient', 'is_main']
    list_display = ['feed','duration','get_small_img_land', 'get_small_img_port', 'get_small_img_square', 'user', 'is_main', 'is_deleted', 'is_approved', 'type_media', 'role_media', 'orient', 'get_img_blur']
    exclude = ['croppos_land']

    
#admin.site.register(UserMedia, UserMediaAdmin)
