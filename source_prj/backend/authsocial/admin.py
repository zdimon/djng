from django.contrib import admin
from .models import SocialAuth
# Register your models here.

@admin.register(SocialAuth)
class SocialAuthAdmin(admin.ModelAdmin):
    list_display = ['userid','type', 'email', 'user']
