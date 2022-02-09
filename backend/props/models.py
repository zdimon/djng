from django.db import models
from django.utils.translation import ugettext_lazy as _
from account.models import UserProfile
from django.utils.safestring import mark_safe

class Props(models.Model):
    TYPE = (
        ('one', _('one')),
        ('many', _('many')),
        ('text', _('text')),
        ('date', _('date'))
    )
    name = models.CharField(
        max_length=250,
        help_text=_('Name'),
        verbose_name=_('Name')
        )
    alias = models.CharField(
        max_length = 250,
        help_text=_('Alias'),
        verbose_name=_('Alias')
        )
    category = models.CharField(
        max_length = 250,
        help_text=_('Category'),
        verbose_name=_('Category')
        )
    type = models.CharField(
        verbose_name=_('Type'),
        choices=TYPE,
        default='one',
        max_length=4)
    for_man = models.BooleanField(
        default=False,
        help_text=_('Show in the man form'),
        verbose_name=_('Show in the man form')
        )
    for_woman = models.BooleanField(
        default=False,
        help_text=_('Show in the woman form'),
        verbose_name=_('Show in the woman form')
        )

    icon = models.ImageField(upload_to='icons')

    @property
    def icon_img(self):
        return mark_safe('<img  src="%s" />' % self.icon.url)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('User property')
        verbose_name_plural = _('User properties')


class Value(models.Model):
    prop = models.ForeignKey(Props, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='icons')
    name = models.CharField(
        max_length=250,
        help_text=_('Name'),
        verbose_name=_('Name')
        )    

    @property
    def icon_img(self):
        return mark_safe('<img  src="%s" />' % self.icon.url)


        
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _('User property value')
        verbose_name_plural = _('User property values')


class Value2User(models.Model):
    prop = models.ForeignKey(Props, on_delete=models.CASCADE)
    value = models.ForeignKey(Value, on_delete=models.CASCADE, null=True, blank=True)
    text_value = models.TextField(default='')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)