from celery import shared_task 
from celery.decorators import task
import json
import redis
from backend.settings import REDIS_HOST, REDIS_PORT
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)
from account.models import UserProfile
from online.models import UserOnline
from chat.rooms_serializer import serialize_messages_by_room, detail_room

@task
def sent_chat_message(room):
    '''
    Sending message to man.
    
    Sending message to woman.
      
    '''

    ######send to man

    man = room.get_payer()
    #print(man)
    sids = UserOnline.get_sids_by_user(man)
    #print(sids)
    data = {
        'task': 'send_chat_message_to_sids',
        'sids': sids,
        'data': detail_room(room,man)
    }
    redis_client.publish('notifications',json.dumps(data))

    ######send to woman

    woman = room.get_woman()
    #print(woman)
    sids = UserOnline.get_sids_by_user(woman)
    #print(sids)
    data = {
        'task': 'send_chat_message_to_sids',
        'sids': sids,
        'data': detail_room(room,woman)
    }
    redis_client.publish('notifications',json.dumps(data))


@task
def send_update_contacts(user):
    '''
       Updating contact list of users after first message.

       @Input: user object.
    '''
    sids = UserOnline.get_sids_by_user(user)
    for s in sids:
        data = {
                'task': 'put_to_socket',
                'data': {
                    'socket_id': s,
                    'action': 'server-action:update_contacts'
                }
        }
        redis_client.publish('notifications',json.dumps(data))


@task
def send_notifications_to_user(instance_id):
    from chat.models import ChatMessage, ChatRoom
    from notifications.models import Notifications
    from chat.serializers import ChatMessageSerializer

    chat_message = ChatMessage.objects.get(pk=instance_id)
    room = ChatRoom.objects.get(pk=chat_message.room.id)
    user = chat_message.user
    abonent = room.get_abonent(user)

    Notifications.objects.create(content_object=chat_message,
                                 user=abonent,
                                 abonent=user,
                                 type='text-chat',
                                 is_readed=False)

    for online in abonent.get_socket_ids():
        data = {
            'task': 'put_to_socket',
            'data': {
                'action': 'server-action:add_chat_message',
                'socket_id': online.sid,
                'data': {
                    'room_id': room.id,
                    'message': ChatMessageSerializer(chat_message).data
                }
            }
        }

        redis_client.publish('notifications', json.dumps(data))

    print(' send_notifications_to_user Done')


@task
def pay_credits_for_video_chat():
    import time
    from chat.models import ChatRoom
    from payment.tasks import send_close_room, send_update_room
    from payment.models import Payment, PaymentType

    for room in ChatRoom.objects.filter(is_video=True):
        if room.is_active:
            t = time.time()
            user = room.get_payer()

            Payment.get_chat_video_payment_or_create(room)
            payment_type = PaymentType.objects.get(alias='video-chat')
            user.deduct(payment_type.price)
            user.save()
            if user.account == 0:
                room.close_room_by_low_account()
                send_update_room(room)
                send_close_room(room)
            elif t - room.activity > 20:
                room.close_room_by_non_activity(room)
                send_close_room(room)
    print('pay_credits_for_video_chat Done')
