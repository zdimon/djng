from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from account.models import UserProfile
from django.utils.safestring import mark_safe


class Agency(models.Model):

    PAYMENT_METHODS = (
        ('pb', _('Privatbank')),
        ('epay', _('Epay'))
    )

    name = models.CharField(
        max_length=250,         
        help_text=_('Name'), 
        verbose_name=_('Name')
    )

    director = models.CharField(
        max_length=250,         
        verbose_name=_('Name and Surname of the Boss')
    )


    address = models.TextField(
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

    phone1 = models.CharField(
        max_length=250, 
        default='',        
        verbose_name=_('Phone 1')
    )

    phone2 = models.CharField(
        max_length=250,         
        default='',
        verbose_name=_('Phone 2')
    )

    term = models.CharField(
        max_length=250,         
        verbose_name=_('Term of work')
    )    

    is_approved = models.BooleanField(default=True)

    def get_admin_url(self):
        return '/admin/agency/agency/%s/change/' % self.id

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')

class AgencyProfile(User):
    PROFILE_TYPES = (
        ('director', _('Director')),
        ('manager', _('Manager'))
    )
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    profile_type = models.CharField(
        verbose_name=_('Language'),
        choices=PROFILE_TYPES,
        default='manager',
        max_length=50)
    name = models.CharField(
        max_length=250,         
        help_text=_('Name'), 
        verbose_name=_('Name')
    )
    phone = models.CharField(
        max_length=250, 
        default='',        
        verbose_name=_('Phone')
    )


class AgencyFiles(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='agency_files', null=True, blank=True)
    video = models.FileField(upload_to='agency_files', null=True, blank=True)
    @property
    def render_image(self):
        if self.image:
            return mark_safe("""<img width="200" src="/media/%s" />""" % self.image)
        if self.video:
            return 'Video file'
    def __str__(self):
        return self.render_image
    class Meta:
        verbose_name = _('Agency file')
        verbose_name_plural = _('Agency files')

class Agency2Woman(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    woman = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    @property
    def admin_icon(self):    
        return mark_safe("""<img width="60" src="%s" />""" % self.woman.main_photo)
    class Meta:
        verbose_name = _('Agency woman')
        verbose_name_plural = _('Agency women')


