from django.db import models
from django.utils.translation import gettext as _


class StaticPage(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    alias = models.CharField(max_length=250, unique=True)
    content = models.TextField(verbose_name=_('Content'))
