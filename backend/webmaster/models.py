from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from account.models import UserProfile
from django.utils.safestring import mark_safe

class Webmaster(User):

    PAYMENT_METHODS = (
        ('pb', _('Privatbank')),
        ('epay', _('Epay'))
    )

    name = models.CharField(
        max_length=250,         
        help_text=_('Name'), 
        verbose_name=_('Name')
    )


    adress = models.TextField(
        max_length=250,         
        help_text=_('Adress'), 
        verbose_name=_('Ardess of the office')
    )

    payment_method = models.CharField(
        verbose_name=_('Language'),
        choices=PAYMENT_METHODS,
        default='pb',
        max_length=50)

    contact_email = models.CharField(
        max_length=250,         
        verbose_name=_('Email')
    )

    skype = models.CharField(
        max_length=250,  
        default='',       
        verbose_name=_('Email')
    )

    other_messanger = models.CharField(
        max_length=250, 
        default='',        
        verbose_name=_('Other messangers'),
        help_text=_('Skype, telegram etc...')
    )

    country = models.CharField(
        max_length=250, 
        default='',        
        verbose_name=_('Country')
    )

    city = models.CharField(
        max_length=250,         
        verbose_name=_('City')
    )

    phone = models.CharField(
        max_length=250, 
        default='',        
        verbose_name=_('Phone 1')
    )

    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Webmaster')
        verbose_name_plural = _('Webmasters')

