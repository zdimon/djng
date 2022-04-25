from payment.models import Payment, PaymentType
from chat.models import ChatRoom
from usermedia.serializers import UserMediaPhotoSerializer, UserMediaVideoSerializer
import datetime
from account.user_serializer import user_serializer
from payment.tasks import send_show_billing
import redis
import json
from backend.settings import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)

def send_update_account(user):
    for online in user.get_socket_ids():
        data =  {
            'task': 'put_to_socket',
            'data': {
                'action': 'server-action:update_session',
                'socket_id': online.sid,
                'user': user_serializer(user)
            }
        }            
        redis_client.publish('notifications',json.dumps(data))
        if(user.account==0):
            send_show_billing(online.sid)

def make_chat_text_payment(message):
    cur_time = int(message.created_at.timestamp())
    prev = message.get_priv_message()
    if prev:
        if prev.user.gender != message.user.gender:
            if prev.user.gender == 'male':
                man = prev.user
                woman = message.user
            else:
                man = message.user
                woman = prev.user
            # import pdb; pdb.set_trace()
            prev_time = int(prev.created_at.timestamp())
            dif = cur_time - prev_time
            print(dif)
            if dif > 60:
                dif = 10
            print(dif)
            payment_type = PaymentType.objects.get(alias='text-chat') 
            cost = (payment_type.price/60) * dif
            cost = "%.2f" % cost
            print(cost)
            p = Payment()
            p.payer = man
            p.type = payment_type
            p.reciver = woman
            p.agency = woman.get_agency()
            p.ammount = cost
            p.save()
            man.deduct(cost)
            man.save()
            print(man.account)
            send_update_account(man)

def check_media_meassage_payment(message_obj,request):
    reciver = message_obj.user
    payer = request.user.userprofile
    if message_obj.object_id > 0:
        obj = message_obj.content_object
        if obj.type_media == 'video':
            tp = PaymentType.objects.get(alias='show-hidden-video')
            serializer = UserMediaVideoSerializer
        if obj.type_media == 'photo':
            serializer = UserMediaPhotoSerializer
            tp = PaymentType.objects.get(alias='show-hidden-photo')
        try:
            payment = Payment.objects.get(reciver = reciver, payer=payer, type=tp, object_id=obj.id)
            out = {'status': 0, 'message': 'Ok', 'media': serializer(obj).data}
        except Exception as e:
            out = {'status': 1, 'message': str(e)}
        return out
    return {'status': 0, 'message': 'Ok'}

def check_user_account_meassage_payment(message_obj,payer):
    if message_obj.object_id > 0:
        #import pdb; pdb.set_trace()
        obj = message_obj.content_object
        if obj.type_media == 'video':
            tp = PaymentType.objects.get(alias='show-hidden-video')
        if obj.type_media == 'photo':
            tp = PaymentType.objects.get(alias='show-hidden-photo')
        if payer.account < tp.price:
            return False
        else:
            return True

def figure_out_woman_from_request(man,request):
    # print(request)
    try:
        room = ChatRoom.objects.get(pk=request['room_id'])
        return room.get_abonent(man)
    except Exception as e:
        print(str(e))
    return False
        


def process_transaction(man, payment_type, request):
    # print(request)
    woman = figure_out_woman_from_request(man,request)
    if woman:
        p = Payment()
        p.payer = man
        p.type = payment_type
        p.reciver = woman
        p.agency = woman.get_agency()
        p.ammount = payment_type.price
        p.save()
        man.account -= payment_type.price
        man.save()
        return p
    return False

def process_transaction_with_message_obj(man, message_obj):
    if message_obj.content_object.type_media == 'video':
        tp = PaymentType.objects.get(alias='show-hidden-video')
    if message_obj.content_object.type_media == 'photo':
        tp = PaymentType.objects.get(alias='show-hidden-photo')
    p = Payment()
    p.payer = man
    p.type = tp
    p.reciver = message_obj.user
    p.agency = message_obj.user.get_agency()
    p.ammount = tp.price
    p.content_object = message_obj.content_object
    p.save()
    man.account -= tp.price
    man.save()
    return p

    