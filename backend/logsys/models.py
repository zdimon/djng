from django.db import models
from django.utils.translation import ugettext_lazy as _


class Log(models.Model):
    TYPES = (
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('detail_gallery', _('detail_gallery'))
    )
    username = models.CharField(max_length=250, db_index=True)
    ip_address = models.CharField(max_length=250, db_index=True)
    user_agent = models.CharField(max_length=250, db_index=True)
    view_name = models.CharField(max_length=250)
    type = models.CharField(verbose_name=_('Type of message'), choices=TYPES, default='login', max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
