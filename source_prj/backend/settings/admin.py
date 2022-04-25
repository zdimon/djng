from django.contrib import admin
from .models import MailTemplates, AppSettings, Pictures, ReplanishmentPlan
from grappelli_modeltranslation.admin import TranslationAdmin


@admin.register(MailTemplates)
class MailAdmin(TranslationAdmin):
    pass


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(Pictures)
class PicturesAdmin(admin.ModelAdmin):
    list_display = ['alias','admin_icon', 'name', 'type_obj']

@admin.register(ReplanishmentPlan)
class ReplanishmentPlanAdmin(admin.ModelAdmin):
    list_display = ['name','dollar', 'credit']