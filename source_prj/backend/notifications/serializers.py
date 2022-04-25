from rest_framework import serializers

from notifications.models import Notifications


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'user', 'abonent', 'created_at', 'type', 'object_id', 'is_readed', 'readed_at']


def notification_serializer(notification):
    from account.user_serializer import user_serializer
    data = {
        "user": user_serializer(notification.user),
        "abonent": user_serializer(notification.abonent),
        "created_at": str(notification.created_at),
        "type": notification.type,
        "object_id": notification.object_id,
        "is_readed": notification.is_readed,
        "readed_at": notification.readed_at,
    }
    return data
