from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Moderation(models.Model):
    TYPE_OBJ = (
        ('woman-profile', _('Woman profile')),
        ('man-profile', _('Man profile')),
        ('agency', _('Agency')),
        ('photo-new', _('New photo')),
        ('photo-delete', _('Delete photo')),
        ('video-new', _('New video')),
        ('video-delete', _('Delete video')),
        ('feed-new', _('New video')),
        ('feed-delete', _('Delete video')),
        ('video', _('Video')),
        ('verify-doc', _('Verification documents')),
    )

    type_obj = models.CharField(
        verbose_name=_('Object type'),
        choices=TYPE_OBJ,
        default='woman-profile',
        max_length=20)

    name = models.CharField(
        max_length=250,         
        default='',
        verbose_name=_('Name')
    )    
    is_new = models.BooleanField(
        verbose_name=_('New or not?'),
        default=True)    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    data = models.TextField(default='[]')

    def __str__(self):
        return self.name

class ModerationFiles(models.Model):
    moderation = models.ForeignKey(Moderation, on_delete=models.CASCADE)
    image = models.FileField(upload_to='moderation_files')