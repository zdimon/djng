from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from backend.settings import LANGUAGES
from online.models import UserOnline
from django.utils.safestring import mark_safe
from backend.settings import DOMAIN
from backend.settings import REDIS_HOST, REDIS_PORT

import redis
import json

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)
from .user_serializer import user_serializer
from datetime import date
from settings.models import ReplanishmentPlan
from .utils import zodiac_sign
from rest_framework.authtoken.models import Token
from django_countries.fields import CountryField
from django.conf import settings
from .tokens import get_token_generator
from decimal import Decimal

from taggit.managers import TaggableManager

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
TOKEN_GENERATOR_CLASS = get_token_generator()


class UserProfile(User):
    GENDER = (
        ('male', _('Man')),
        ('female', _('Woman'))
    )
    about_me = models.TextField(
        help_text=_('About me'),
        verbose_name=_('About me'))

    language = models.CharField(
        verbose_name=_('Language'),
        choices=LANGUAGES,
        default='en',
        max_length=2)

    gender = models.CharField(
        verbose_name=_('Gender'),
        choices=GENDER,
        db_index=True,
        default='male',
        max_length=6)

    publicname = models.CharField(default='', max_length=250)
    lastname = models.CharField(default='', max_length=250, null=True, blank=True)
    is_online = models.BooleanField(default=False)
    account = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    birthday = models.DateField(null=True, blank=True)
    lookingfor = models.TextField(default='', null=True, blank=True)
    goal = models.TextField(default='', null=True, blank=True)
    job = models.TextField(default='', null=True, blank=True)
    city = models.CharField(default='', max_length=250)
    country = CountryField(default='UA')
    zodiac = models.CharField(default='', max_length=50)
    is_camera = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    tags = TaggableManager()

    def deduct(self,ammount):
        self.account = self.account - Decimal(ammount)
        print(self.account)
        if self.account < 0:
            self.account = 0
        self.save()


    def get_token(self):
        try:
            token = Token.objects.get(user=self)
            return str(token)
        except:
            return None

    def save(self, *args, **kwargs):
        self.zodiac = zodiac_sign(self)
        super(UserProfile, self).save(*args, **kwargs)

    def check_subscription(self, destination):
        from feed.models import UserFeedSubscription
        # import pdb; pdb.set_trace()
        try:
            UserFeedSubscription.objects.get(user_subscriber=self, user_destination=destination)
            return True
        except Exception as e:
            # print(e)
            return False

    def get_agency(self):
        from agency.models import Agency2Woman
        if self.gender == 'female':
            try:
                a2w = Agency2Woman.objects.get(woman=self)
                return a2w.agency
            except:
                return None
        return None

    def getOppositeGender(self):
        if self.gender == 'male':
            return 'female'
        else:
            return 'male'

    def getLastFeed(self):
        from feed.models import UserFeed
        try:
            return UserFeed.objects.filter(user=self, is_approved=True).order_by('-id')[0]
        except Exception as e:
            # print(str(e))
            return None

    @property
    def age(self):
        today = date.today()
        try:
            return today.year - self.birthday.year - (
                    (today.month, today.day) < (self.birthday.month, self.birthday.day))
        except:
            return 0

    @property
    def zodiac_icon(self):
        return mark_safe('<img width="60" src="/static/images/icons/zodiac/%s.png" />' % self.zodiac)

    # @property
    # def zodiak(self):
    #    return zodiac_sign(self.birthday)

    # def make_zodiak(self):
    #    self.zodiac = zodiac_sign(self)
    #    self.save()

    @staticmethod
    def get_user_by_name(name):
        try:
            return UserProfile.objects.get(username=name)
        except Exception as Err:
            print(Err)
            return None

    @property
    def main_photo(self):
        from usermedia.models import UserMedia
        try:
            photo = UserMedia.objects.get(user=self, is_main=True, type_media='photo')
            return photo.get_small_url_square

        except Exception as Err:
            return DOMAIN + '/static/images/empty_%s.jpeg' % self.gender

    @property
    def middle_photo(self):
        from usermedia.models import UserMedia
        try:
            photo = UserMedia.objects.get(user=self, is_main=True, type_media='photo')
            return photo.get_middle_url_square
        except Exception as Err:
            return DOMAIN + '/static/images/empty_%s.jpeg' % self.gender

    @property
    def main_photo_port(self):
        from usermedia.models import UserMedia
        try:
            photo = UserMedia.objects.get(user=self, is_main=True, type_media='photo')
            return photo.get_small_url_port

        except Exception as Err:
            return DOMAIN + '/static/images/empty_%s.jpeg' % self.gender

    @property
    def middle_photo(self):
        from usermedia.models import UserMedia
        try:
            photo = UserMedia.objects.get(user=self, is_main=True, type_media='photo')
            if photo.orient == 'land':
                return photo.get_middle_url_land
            else:
                return photo.get_middle_url_port
        except Exception as Err:
            return DOMAIN + '/static/images/empty_%s.jpeg' % self.gender

    @property
    def admin_icon(self):
        return mark_safe("""<img width="60" src="%s" />""" % self.main_photo)

    @property
    def is_subscribed(self):
        return False

    def get_socket_ids(self):
        return UserOnline.objects.filter(user=self)

    def set_offline(self):
        self.is_online = False
        self.save()
        data = {
            'task': 'user_offline',
            'user': {self.id: user_serializer(self)}
        }
        redis_client.publish('notifications', json.dumps(data))

    def set_online(self):
        self.is_online = True
        self.save()
        data = {
            'task': 'user_online',
            'user': {self.id: user_serializer(self)}
        }
        redis_client.publish('notifications', json.dumps(data))


class UserProfileDoc(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='profile_docs', null=True, blank=True)
    image2 = models.ImageField(upload_to='profile_docs', null=True, blank=True)
    first_name = models.CharField(default='', max_length=250)
    last_name = models.CharField(default='', max_length=250)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_admin_url(self):
        return '/admin/account/userprofiledoc/%s/change/' % self.id

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Profile verify files')
        verbose_name_plural = _('Profile verify file')


class ReplenishmentLog(models.Model):
    user_profile = models.ForeignKey(UserProfile, default='', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(ReplanishmentPlan, null=True, on_delete=models.SET_NULL)
    # subscription that used for the plan actually (even from different plan)
    bonus_subscription = models.ForeignKey('subscription.BonusSubscription', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user_profile.email


class ResetPasswordToken(models.Model):
    class Meta:
        verbose_name = _('Password Reset Token')
        verbose_name_plural = _('Password Reset Tokens')

    @staticmethod
    def generate_key():
        return TOKEN_GENERATOR_CLASS.generate_token()

    id = models.AutoField(
        primary_key=True
    )

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='password_reset_tokens',
        on_delete=models.CASCADE,
        verbose_name=_('The User which is associated to this password reset token')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('When was this token generated')
    )

    key = models.CharField(
        _('Key'),
        max_length=64,
        db_index=True,
        unique=True
    )

    ip_address = models.GenericIPAddressField(
        _('The IP address of this session'),
        default='',
        blank=True,
        null=True
    )

    user_agent = models.CharField(
        max_length=256,
        verbose_name=_('HTTP user Agent'),
        default='',
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ResetPasswordToken, self).save(*args, **kwargs)

    def __str__(self):
        return 'Password reset token for user {user}'.format(user=self.user)


class LoginWarningHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    previous_ok_ip_address = models.GenericIPAddressField()
    current_warning_ip_address = models.GenericIPAddressField()
    current_country = models.CharField(max_length=250)
    current_city = models.CharField(max_length=250, blank=True)
    full_current_location_info = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


def get_password_reset_token_expiry_time():
    return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPITY_TIME', 24)


def get_password_reset_lookup_field():
    return getattr(settings, 'DJANGO_REST_LOOKUP_FIELD', 'email')


def clear_expired(expiry_time):
    ResetPasswordToken.objects.filter(created_at__lte=expiry_time).delete()


def eligible_for_reset(self):
    if not self.is_active:
        return False

    if getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_REQUIRE_USABLE_PASSWORD', True):
        return self.has_usable_password()
    else:
        return True


UserModel = get_user_model()
UserModel.add_to_class('eligible_for_reset', eligible_for_reset)
