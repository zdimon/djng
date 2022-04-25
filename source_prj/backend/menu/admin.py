from django.contrib import admin
from .models import Menu2User, Menu
# Register your models here.




class Menu2UserAdmin(admin.StackedInline):
    model = Menu2User
    fields = ('menu', 'user', 'can_edit', 'can_delete', 'can_create')
    raw_id_fields  = ['user']



class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'icon', 'page']
    inlines = [ Menu2UserAdmin ]


admin.site.register(Menu, MenuAdmin)
