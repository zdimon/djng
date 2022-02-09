from rest_framework import serializers

from .models import Agency


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = 'name', 'director', 'address', 'payment_method', \
                 'contact_email', 'skype', 'other_messanger', 'country', 'city', \
                 'is_approved', 'term', 'phone1', 'phone2'
