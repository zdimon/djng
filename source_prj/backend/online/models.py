from django.db import models
import time
# Create your models here.
from django.contrib.auth.models import User
import asyncio

class UserOnline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=250, db_index=True)
    sid = models.CharField(max_length=250, db_index=True)
    token = models.CharField(max_length=250, db_index=True, null=True)
    agent = models.CharField(max_length=250, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    activity = models.IntegerField(default=0)

    @staticmethod
    def get_sids_by_user(user):
        sids = []
        for user in UserOnline.objects.filter(user=user):
            sids.append(user.sid)
        return sids
    
    @staticmethod
    async def set_online(login,sid):
        
        try:
            uo = UserOnline.objects.get(username=login)
        except:
            user = User.objects.get(username=login)
            uo = UserOnline()
            uo.username = login
            uo.user = user
        uo.sid = sid
        uo.save() 

    def save(self, *args, **kwargs):
        if not self.id:
            self.activity = time.time()
        super(UserOnline, self).save(*args, **kwargs)

            
