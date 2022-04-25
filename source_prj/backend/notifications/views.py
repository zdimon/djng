from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, pagination

from notifications.models import Notifications
from account.models import UserProfile
from notifications.serializers import NotificationSerializer


class NotificationsView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer
    queryset = Notifications.objects.all()
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        type_notifications = self.kwargs['type']
        profile = UserProfile.objects.get(pk=self.request.user.id)
        if type_notifications == 'chat':
            read_notifications(Notifications.objects.filter(user=profile, type='text-chat'))
            return Notifications.objects.filter(user=profile, type='text-chat')
        elif type_notifications == 'events':
            read_notifications(Notifications.objects.filter(user=profile).exclude(type='text-chat'))
            return Notifications.objects.filter(user=profile).exclude(type='text-chat')


def read_notifications(data):
    for n in data:
        if not n.is_readed:
            n.is_readed = True
            n.readed_at = datetime.now()
            n.save()
