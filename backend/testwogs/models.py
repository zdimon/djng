from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
import json

class ManageLogserver(models.Manager):

    def save_new_record(self, server_status, url_request, request, response, test_status='successfully',
                        alias='No message', api_status=0, method=''):
        new_record = Logserver(server_status=server_status, api_status=api_status, request=request, response=response,
                               alias=alias, url_request=url_request, test_status=test_status, method=method)
        new_record.save()
        return new_record


class Logserver(models.Model):
    url_request = models.CharField(max_length=200, default='')
    test_status = models.CharField(max_length=200, default='successfully')
    server_status = models.SmallIntegerField(default=0)
    api_status = models.SmallIntegerField(default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    alias = models.CharField(max_length=1000, default='No message')
    time_create = models.TimeField(auto_now_add=True)
    request = models.TextField(default='')
    response = models.TextField(default='')
    is_ok = models.BooleanField(default=True)
    method = models.CharField(max_length=200, default='GET')
    objects = ManageLogserver()


@receiver(pre_save, sender=Logserver)
def do_checks(sender, instance, **kwargs):
    if instance.server_status != 200:
        instance.is_ok = False

    try:
        dt = json.loads(self.response)
        if dt["status"] == 1:
            instance.is_ok = False
    except:
        pass