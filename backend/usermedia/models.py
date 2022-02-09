
from django.db import models
from account.models import UserProfile
from image_cropping.fields import ImageRatioField, ImageCropField
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from backend.local import DOMAIN
from django.dispatch import receiver
import os
from django.utils.translation import ugettext_lazy as _
from backend.settings import DOMAIN
from core.mixins.image import ImageModelMixin
from core.mixins.video import VideoModelMixin


class UserMedia(ImageModelMixin, VideoModelMixin, models.Model):
    TYPE_MEDIA = (
        ('photo', _('Photo')),
        ('video', _('Video'))
    )

    ORIENTATION = (
        ('land', _('Landscape')),
        ('port', _('Portrait'))
    )

    ROLE_MEDIA = (
        ('public', _('Public')),
        ('private', _('Private')),
        ('buffer', _('Buffer'))
    )

    type_media = models.CharField(
        verbose_name=_('Type of media'),
        choices=TYPE_MEDIA,
        default='photo',
        max_length=5)

    role_media = models.CharField(
        verbose_name=_('Role of media'),
        choices=ROLE_MEDIA,
        default='public',
        max_length=10)

    orient = models.CharField(
        verbose_name=_('Orientation'),
        choices=ORIENTATION,
        default='port',
        max_length=5)

    feed = models.ForeignKey('feed.UserFeed', on_delete=models.CASCADE, null=True, related_name='feedmedia')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    price = models.IntegerField(default=0, null=True, blank=True)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    geolocation = models.CharField(max_length=250)
    to_the_stories = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_media+str(self.id)

    @property
    def get_admin_url(self):
        return '/admin/usermedia/usermedia/%s/change/' % self.id




    def setAsMain(self):
        UserMedia.objects.filter(user=self.user).update(is_main=False)
        self.is_main = True
        self.save()

    def __str__(self):
        try:
            thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
                'size': (50, 50),
                'box': self.cropping_port,
                'crop': 'smart',
                'upscale': True,
            }).url
            return mark_safe('<img src="%s" />' % thumbnail_url)
        except:
            return 'none'


@receiver(models.signals.post_delete, sender=UserMedia)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `ImageModel` object is deleted.
    """
    if instance.image:
        thumbmanager = get_thumbnailer(instance.image)
        thumbmanager.delete(save=False)
        try:
            path = instance.image.path
            os.remove(path)
        except:
            pass

    if instance.video:
        try:
            path = instance.video.path
            os.remove(path)
        except:
            pass

