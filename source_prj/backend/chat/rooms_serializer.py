from account.serializers import UserSerializer
from rest_framework.response import Response
from account.user_serializer import user_serializer
from account.models import UserProfile
from backend.exeptions.chatexeption import ChatContactException


def serialize_message(m):
    mes = {
            'id': m.id,
            'message': m.message,
            'author_id': m.user.id,
            'is_private': m.is_private,
            'created': str(m.created_at),
            'is_readed': m.is_readed
        }
    return mes


def serialize_messages_by_room(room):
    from chat.models import ChatMessage
    out = {}
    for m in ChatMessage.objects.filter(room=room).order_by('-id'):
        out[m.id] = serialize_message(m)
    return out


def detail_room(room,user):
    from chat.models import ChatMessage, ChatContact

    res = {}
    try:
        abonent = ChatContact.objects.filter(room=room).exclude(abonent=user)[0]
    except:
        # raise ChatContactException('Can`t select abonent room_serializer.detail_room!')
        room.delete()
        return {'status': 1, 'message': 'error abonent'}
    res['abonent_id'] = abonent.abonent.id
    res['id'] = room.id
    res['is_current'] = abonent.is_current
    res['is_active'] = room.is_active
    res['is_low_account'] = room.is_low_account
    res['activity'] = room.activity
    res['is_abonent_camera'] = abonent.is_camera
    mes = {}
    for m in ChatMessage.objects.filter(room=room).order_by('-id')[0:5]:
        mes[m.id] = serialize_message(m)
    res['messages'] = mes
    return res


def get_current_room(user):
    from chat.models import ChatContact

    for c in ChatContact.objects.filter(owner=user):
        if c.is_current:
            return c.room.id


def serialize_rooms(user):
    from chat.models import ChatContact

    rooms_ids = []
    contacts_ids = []
    online_ids = []
    contact_users = {}
    rooms_list = {}       
    current_room = {}

    # select online users
    # online = UserProfile.objects.filter(is_online=True, gender=user.getOppositeGender())
    # for o in online:
    #     online_ids.append(o.id)

    contacts = ChatContact.objects.filter(owner=user)
    for c in contacts:
        rooms_ids.append(c.room.id)
        #contact_users[c.abonent.id] = user_serializer(c.abonent)
        #contact_users[c.owner.id] = user_serializer(c.owner) 
    # for c in contacts:
    #     contacts_ids.append(c.abonent.id)
    # contacts_ids.append(user.id)

    for c in contacts:
        rooms_list[c.room.id] = detail_room(c.room,user)   
    return {
        'room_ids': rooms_ids, 
        'rooms': rooms_list, 
        'contacts_ids': contacts_ids,
        'online_ids': online_ids,
        'contact_users': contact_users,
        'current_room': get_current_room(user)
    }
