from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from backend.settings import LANGUAGES
from django.utils.translation import ugettext_lazy as _
# Register your models here.


class AdminProfile(User):

    language = models.CharField(
    verbose_name=_('Language'),
    choices=LANGUAGES,
    default='en',
    max_length=2)