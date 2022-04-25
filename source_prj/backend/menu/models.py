from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    icon = models.CharField(max_length=250)
    page = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Menu2User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)