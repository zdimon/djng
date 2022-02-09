import json
import redis

from celery.decorators import task
from backend.settings import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)


@task
def add_notification_likes(instance_id):
    print('add_notification_likes')
    from likes.models import Likes
    from account.models import UserProfile
    from feed.models import UserFeed
    from notifications.models import Notifications
    from chat.models import ChatRoom
    from account.user_serializer import user_serializer
    from notifications.serializers import notification_serializer

    instance = Likes.objects.get(pk=instance_id)
    id_user = UserFeed.objects.get(pk=instance.content_object.id).user.id

    user = UserProfile.objects.get(pk=id_user)
    user_like = UserProfile.objects.get(pk=instance.liker.id)

    room_id = ChatRoom.get_room_or_create(user, user_like).id

    notification = Notifications.objects.create(content_object=instance,
                                                user=user,
                                                abonent=user_like,
                                                type='like',
                                                is_readed=False)
    serialized_user = user_serializer(user)
    user_like = user_serializer(user_like)
    notification = notification_serializer(notification)
    for online in instance.liker.get_socket_ids():
        data = {
            'task': 'put_to_socket',
            'data': {
                'action': 'server-action:add_like',
                'socket_id': online.sid,
                'data': {
                    'room_id': room_id,
                    'user': serialized_user,
                    'user_like': user_like,
                    'notification': notification
                }
            }
        }

        redis_client.publish('notifications', json.dumps(data))
    print('add_notification_likes Done')
