from django.contrib import admin
from .models import Offer, Ice, Connection
# Register your models here.


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user']

admin.site.register(Connection, ConnectionAdmin)


class OfferAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'offer']

admin.site.register(Offer, OfferAdmin)



class IceAdmin(admin.ModelAdmin):
    list_display = ['offer', 'ice']

admin.site.register(Ice, IceAdmin)