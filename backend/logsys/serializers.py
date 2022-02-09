from rest_framework import serializers
from .models import Log


class LogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(input_formats=['%d-%m-%Y %h',])
    class Meta:
        model = Log
        fields = 'id', 'username', 'ip_address', 'user_agent', 'view_name', 'type', 'created_at'
