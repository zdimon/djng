from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from account.models import UserProfile


class Notifications(models.Model):
    TYPES = (('text-chat', 'Text chat'),
             ('like', 'Like'),
             ('subscribe', 'Subscribe'),
             ('comment', 'Comment'),
             ('block', 'Block'))

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user')
    abonent = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_abonent')
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TYPES, default='text-chat')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    is_readed = models.BooleanField(default=False)
    readed_at = models.DateTimeField(null=True)
