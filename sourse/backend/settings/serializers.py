from rest_framework import serializers
from settings.models import ReplanishmentPlan, Pictures


class ReplanishmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplanishmentPlan
        fields = 'id', 'name', 'dollar', 'credit', 'curency'
        

class SmileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = 'id', 'name', 'alias', 'image', 'type_obj'