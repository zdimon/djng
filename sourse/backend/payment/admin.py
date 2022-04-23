from django.contrib import admin
from account.admin import superadmin_site
# Register your models here.
from .models import Payment, PaymentType
# Register your models here.

@admin.register(Payment, site=superadmin_site)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payer', 'reciver', 'ammount', 'type', 'agency', 'is_closed', 'content_object', 'created_at']
admin.site.register(Payment, PaymentAdmin)

@admin.register(PaymentType, site=superadmin_site)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'alias', 'price']
admin.site.register(PaymentType, PaymentTypeAdmin)