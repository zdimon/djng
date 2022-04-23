from rest_framework import serializers
from .models import Likes


class LikeSerializer(serializers.ModelSerializer):
    #obj_model = serializers.CharField(required=False, allow_blank=True, max_length=100)
    class Meta:
        model = Likes
        fields = ['id', 'content_type', 'object_id']