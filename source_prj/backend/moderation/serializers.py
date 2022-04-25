from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from moderation.models import Moderation


class ModerationSerializer(serializers.ModelSerializer):
    content_object = SerializerMethodField()

    def get_content_object(self, obj):
        content_object = obj.content_object.__class__.__name__
        return content_object

    class Meta:
        model = Moderation
        fields = ['id', 'type_obj', 'name', 'is_new', 'object_id', 'data', 'content_object']
