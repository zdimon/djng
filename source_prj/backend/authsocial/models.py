from django.db import models
from account.models import UserProfile
# Create your models here.

class SocialAuth(models.Model):
    type = models.CharField(max_length=50)
    userid = models.CharField(max_length=250)
    email =  models.CharField(max_length=50)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE) 