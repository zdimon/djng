from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

class MailTemplates(models.Model):
    alias = models.CharField(max_length=250, unique=True)
    title = models.CharField(max_length=250)
    content = models.TextField(
        help_text=_('Content'), 
        verbose_name=_('Content'))

    def parse(self, data):
        for var in data:
            self.content = self.content.replace(var['name'], var['value'])

    def __str__(self):
        return self.title


class AppSettings(models.Model):
    alias = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Pictures(models.Model):
    name = models.CharField(max_length=250)
    alias = models.CharField(max_length=250)
    type_obj = models.CharField(max_length=250)
    image = models.ImageField(upload_to='pictures')
    @property
    def admin_icon(self):
        return mark_safe('<img src="%s" />' % self.image.url)


class ReplanishmentPlan(models.Model):
    CURENCY = (
        ('US', _('US')),
        ('EUR', _('EUR'))
    )
    curency = models.CharField(
        verbose_name=_('Curency'),
        choices=CURENCY,
        default='US',
        max_length=5)
    name = models.CharField(max_length=250)
    dollar = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    # default bonus subscription for the plan (compare with ReplanishmentLog)
    bonus_subscription = models.ForeignKey('subscription.BonusSubscription', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
