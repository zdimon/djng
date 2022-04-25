from django.db import models
from django.dispatch import receiver

from account.models import UserProfile
from django.utils.translation import ugettext_lazy as _
import time

from chat.tasks import send_notifications_to_user
from payment.models import Payment
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class ChatRoom(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False, verbose_name=_('Is active?'))
    is_answered = models.BooleanField(default=False, verbose_name=_('Is answered?'))
    is_low_account = models.BooleanField(default=False, verbose_name=_('Is low account?'))
    is_video = models.BooleanField(default=False, verbose_name=_('Is video?'))
    activity = models.IntegerField(default=0)

    def mark_as_readed(self,user):
        for m in ChatMessage.objects.filter(user=self.get_abonent(user)):
            m.mark_as_readed()

    def is_current(self,owner):
        contact = ChatContact.objects.get(room=self,owner=owner)
        if contact.is_current:
            return True
        return False

    
    def check_first_message(self):
        if ChatMessage.objects.filter(room=self).count()==1:
            return True
        else:
            return False

    @staticmethod
    def get_room_or_create(owner, abonent):
        '''
        Create or select and return the room object.
        '''
        try:
            c = ChatContact.objects.get(owner=owner, abonent=abonent)
            c.set_current()
            return c.room
        except:
            room = ChatRoom()
            room.save()
            contact = ChatContact()
            contact.owner = owner
            contact.abonent = abonent
            contact.room = room
            contact.save()
            contact.set_current()
            contact = ChatContact()
            contact.owner = abonent
            contact.abonent = owner
            contact.room = room
            contact.save()
            return room

    def get_abonent(self,user):
        contact = ChatContact.objects.filter(room=self).exclude(owner=user)[0]
        return contact.owner

    def get_payer(self):
        contacts = ChatContact.objects.filter(room=self)
        for c in contacts:
            if c.owner.gender == 'male':
                return c.owner

    def get_woman(self):
        contacts = ChatContact.objects.filter(room=self)
        for c in contacts:
            if c.owner.gender == 'female':
                return c.owner       

        return contact.owner

    def check_is_active_by_message(self,message):
        '''
            Checking for answering.
        '''
        author = message.user
        if author.gender=='male' and self.is_answered:
            self.is_active = True
            self.save()  
            return True          
        try:
            # check if woman answer first time
            am = ChatMessage.objects.filter(room=self).exclude(pk=message.id).order_by('-id')[0]
            if am.user != message.user and not self.is_answered:
                self.is_active = True
                self.is_answered = True
                self.save() 
        except:
            self.is_active = False
            self.save()

    def close_room_by_low_account(self):
        self.is_active = False
        self.is_low_account = True
        self.save()
        p = Payment.get_chat_text_payment_or_create(self)
        p.is_closed = True
        p.save()
        p = Payment.get_chat_video_payment_or_create(self)
        p.is_closed = True
        p.save()

    def close_room_by_stop_button(self):
        self.is_active = False
        self.is_low_account = False
        self.save()
        p = Payment.get_chat_text_payment_or_create(self)
        p.is_closed = True
        p.save()

    def close_room_by_non_activity(self):
        self.is_active = False
        self.is_low_account = False
        self.save()
        p = Payment.get_chat_video_payment_or_create(self)
        p.is_closed = True
        p.save()

    def save(self, *args, **kwargs):
        self.activity = time.time()
        super(ChatRoom, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Chat room')
        verbose_name_plural = _('Chat rooms')


class ChatContact(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="owner")
    abonent = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name="abonent")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_current = models.BooleanField(default=False)
    is_camera = models.BooleanField(default=False)


    def set_current(self):
        for c in ChatContact.objects.filter(owner=self.owner):
            c.is_current = False
            c.save()
        self.is_current = True
        self.save()        


class ChatMessage(models.Model):

    TYPES = (
        ('message', _('message')),
        ('video', _('video')),
        ('image', _('image')),
        ('sticker', _('sticker')),
        ('post', _('post'))
    )
    type = models.CharField(
        verbose_name=_('Type of message'),
        choices=TYPES,
        default='message',
        max_length=10)

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_readed = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def get_priv_message(self):
        try:
            return ChatMessage.objects.filter(room=self.room,pk__lt=self.id).order_by('-id')[0]
        except:
            return None
    
    def save(self, *args, **kwargs):
        room = self.room
        room.activity = time.time()
        room.save()
        super(ChatMessage,self).save(*args, **kwargs)

    def mark_as_readed(self):
        self.is_readed = True
        self.save()


@receiver(models.signals.post_save, sender=ChatMessage)
def send_notifications(sender, instance, **kwargs):
    send_notifications_to_user.delay(instance.id)


class ChatSession(models.Model):
    TYPES = (
        ('text', _('Text chat')),
        ('man_video', _('Man video')),
        ('woman_video', _('Woman video'))
    )
    type = models.CharField(
        verbose_name=_('Type of session'),
        choices=TYPES,
        default='text',
        max_length=12)

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
