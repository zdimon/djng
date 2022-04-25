from backend.settings import REDIS_HOST, REDIS_PORT
import redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)
from online.models import UserOnline
from django.utils.translation import ugettext_lazy as _
import json
from chat.models import ChatContact
from payment.tasks import send_show_billing


def send_notify_about_low_account(user):
    for sid in user.get_socket_ids():
        send_show_billing(sid.sid)



def mark_room_as_current(room,owner):
    c = ChatContact.objects.get(owner=owner,room=room)
    c.set_current() 

def check_man_account(room):
    payer = room.get_payer()
    if payer.account<4:
        return False
    else:
        return True

def send_notification_to_woman(room):
    pass
    '''
    woman = room.get_woman()
    sids = UserOnline.get_sids_by_user(woman)
    message = _('Sorry you can not send message')
    data = {
        'task': 'send_chat_message_to_sids',
        'sids': sids,
        'message': '%s' % message,
        'user': {'username': 'moderator', 'main_photo': 'test'},
        'room_id': room.id,
        'time': '123'
    }
    print(data)
    redis_client.publish('notifications',json.dumps(data))
    '''
