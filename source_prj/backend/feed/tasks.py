from celery.decorators import task
import cv2
from backend.settings import DOMAIN, BASE_DIR, REDIS_HOST, REDIS_PORT
from django.core.files import File
import redis
import json
from backend.settings import REDIS_HOST, REDIS_PORT

from celery.task import periodic_task
from celery.schedules import crontab



redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)


@task
def take_pic_from_video(media):
    cam = cv2.VideoCapture(media.video.path)
    ret,frame = cam.read()
    path = '%s/tmp/%s.jpg' % (BASE_DIR,media.id)
    print ('Creating...' + path)
    cv2.imwrite(path, frame)
    try:
        with open(path, 'rb') as image:
            media.image.save('%s.jpg'% media.id, File(image), save=True)
            media.save()
    except Exception as ex:
        print(ex)


@task
def add_notification_comment(instance_id):
    from feed.models import UserFeedComment
    from account.models import UserProfile
    from chat.models import ChatRoom
    from feed.serializers import user_feed_serializer
    from account.user_serializer import user_serializer
    from notifications.models import Notifications
    from notifications.serializers import notification_serializer
    instance = UserFeedComment.objects.get(pk=instance_id)

    id_user_feed = instance.feed.user_id
    id_user_commented = instance.user.id

    user = UserProfile.objects.get(pk=id_user_feed)
    comment_user = UserProfile.objects.get(pk=id_user_commented)
    room_id = ChatRoom.get_room_or_create(user, comment_user).id
    comment = UserFeedComment.objects.get(pk=instance.id)

    notification = Notifications.objects.create(content_object=instance,
                                                user=user,
                                                abonent=comment_user,
                                                type='comment',
                                                is_readed=False)


    user_serialised = user_serializer(user)
    try:
        comment = user_feed_serializer(comment)
    except Exception as ex:
        print(ex)
    notification = notification_serializer(notification)
    for online in user.get_socket_ids():
        
        data = {
            'task': 'put_to_socket',
            'data': {
                'action': 'server-action:add_comment_to_chat_room',
                'socket_id': online.sid,
                'data': {
                    'room_id': room_id,
                    'user': user_serialised,
                    'comment': comment,
                    'notification': notification
                }
            }
        }
        redis_client.publish('notifications', json.dumps(data))



@task
def repost_to_chat(comment_id):
    from feed.models import UserFeedComment
    from chat.models import ChatMessage
    from chat.models import ChatRoom
    comment = UserFeedComment.objects.get(pk=comment_id)
    print(comment)
    reciver = comment.feed.user
    commentator = comment.user
    room = ChatRoom.get_room_or_create(reciver, commentator)
    m = ChatMessage()
    m.type = 'post'
    m.message = 'new post'
    m.user = commentator
    m.room = room
    m.content_object = comment
    m.save()
    print('repost_to_chat Done')


@task
def add_notification_subscription(instance_id):
    from feed.models import UserFeedSubscription
    from account.models import UserProfile
    from notifications.serializers import notification_serializer
    from account.user_serializer import user_serializer
    from chat.models import ChatRoom
    from notifications.models import Notifications
    instance = UserFeedSubscription.objects.get(pk=instance_id)

    user_destination = UserProfile.objects.get(pk=instance.user_destination.id)
    user_subscriber = UserProfile.objects.get(pk=instance.user_subscriber.id)

    room_id = ChatRoom.get_room_or_create(user_destination, user_subscriber).id

    notification = Notifications.objects.create(content_object=instance,
                                                user=user_destination,
                                                abonent=user_subscriber,
                                                type='subscribe',
                                                is_readed=False)

    serialized_user_destination = user_serializer(user_destination)
    try:
        user_subscriber = user_serializer(user_subscriber)
    except Exception as ex:
        print(ex)
    notification = notification_serializer(notification)
    for online in user_destination.get_socket_ids():
        data = {
            'task': 'put_to_socket',
            'data': {
                'action': 'server-action:add_subscription',
                'socket_id': online.sid,
                'data': {
                    'id': instance_id,
                    'user_id': user_destination.id,
                    'user_dest': serialized_user_destination,
                    'user_sub': user_subscriber,
                    'notification': notification
                }
            }
        }

        redis_client.publish('notifications', json.dumps(data))
    print('add_notification_subscription Done')


"""
    We remove from the stories media content that has exhausted its lifetime (24 hours).
    If all content is removed from the story, the story becomes a regular post.
    (every 5 minutes)
"""

@periodic_task(ignore_result=True, run_every=crontab(minute='*/5'))
def check_empty_stories():
    from datetime import datetime, timedelta
    import pytz
    from feed.models import UserFeed
    from usermedia.models import UserMedia
    feed_list = UserFeed.objects.filter(is_stories=True).only('id')
    if feed_list:
        for feed in feed_list:
            media_list = UserMedia.objects.filter(feed_id=feed.id).only('created_at')
            len_media_list = len(media_list)
            count_delete = 0
            now = pytz.utc.localize(datetime.now())
            for m in media_list:
                table_expire_datetime = m.created_at + timedelta(days=1)
                if table_expire_datetime > now:
                    continue
                else:
                    m.to_the_stories = False
                    m.save()
                    count_delete += 1
            if len_media_list == count_delete:
                feed.is_stories = False
                feed.save()