from django.db import models
from account.models import UserProfile
from chat.models import ChatRoom
import json
# Create your models here.

class Connection(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_from')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_to')
    owner_sdp = models.TextField(default='')
    abonent_sdp = models.TextField(default='')
    owner_ice = models.TextField(default="[]")
    abonent_ice = models.TextField(default="[]")

    def set_offer(self,offer):
        'Setting offer to connection.'
        self.abonent_sdp = offer
        self.abonent_ice = json.dumps([])
        self.save()

    def set_answer(self,answer):
        'Setting answer to connection.'
        self.owner_sdp = answer
        self.owner_ice = json.dumps([])
        self.save()

    def set_owner_ice(self,ice):
        'Setting ice for offer.'
        old = json.loads(self.owner_ice)
        old.append(ice)
        self.owner_ice = json.dumps(old)
        self.save()

    def set_abonent_ice(self,ice):
        'Setting ice for answer.'
        old = json.loads(self.abonent_ice)
        old.append(ice)
        self.abonent_ice = json.dumps(old)
        self.save()

    @staticmethod
    def create_con_if_not_exist(owner,abonent):
        try:
            con = Connection.objects.get(from_user=abonent, to_user=owner, room=room)
        except:
            con = Connection()
            con.from_user = abonent
            con.to_user = owner
            con.save()
        return con

    @staticmethod
    def remove_con(owner,abonent):
        try:
            con = Connection.objects.get(from_user=abonent, to_user=owner, room=room)
            con.delete()
        except:
            pass

    @staticmethod
    def get_con_by_from_user(user):
        try:
            conn = Connection.objects.get(from_user=user)
        except:
            return None
        return conn

    @staticmethod
    def get_con_by_to_user(user):
        try:
            conn = Connection.objects.get(to_user=user)
        except:
            return None
        return conn


class Offer(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)
    offer = models.TextField(default='')


class Ice(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    ice = models.TextField(default='')


class ActiveStream(models.Model):
    session_id = models.CharField(max_length=100)
    session_status = models.BooleanField(default=0)
    session_created_at = models.DateTimeField()

    user_profile = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)