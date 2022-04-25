from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from account.models import UserProfile
from likes.tasks import add_notification_likes


class Likes(models.Model):
    liker = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = 'liker', 'content_type', 'object_id'


@receiver(post_save, sender=Likes)
def inc_like_counter(sender, instance, **kwargs):
    print('Saving likes')
    add_notification_likes.delay(instance.id)
    if hasattr(instance.content_object, 'likes'):
        instance.content_object.likes += 1
        instance.content_object.save()
