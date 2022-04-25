from celery import shared_task 
from celery.decorators import task
import json
from .utils import set_user_offline
import redis
import json


import socketio
import json
import sys
import redis
import time
from datetime import datetime
from backend.settings import SOCKET_SERVER
from online.models import UserOnline
from online.utils import set_user_offline
from account.models import UserProfile
from backend.settings import REDIS_HOST, REDIS_PORT


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)

@task
def publish_to_redis(data):
    print('Publish to redis task')
    redis_client.publish('notifications',json.dumps(data))



@task 
def remove_offline():
    print('removing offline....')
    for uo in UserOnline.objects.all():
        now = time.time()-60
        if uo.activity<now and uo.activity>0:
            is_removed = True
            pr = uo.user.userprofile
            print('Removing %s '% pr.username)
            pr.set_offline()
            uo.delete()
    
@task 
def update_online():
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    print('send gathering')
    data = {'task': 'gather_active_connections'}
    redis_client.publish('notifications', json.dumps(data))
    time.sleep(2)
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)
    redis_online = json.loads(redis_client.get('socket_connections').decode('utf-8'))
    print(redis_online)
    
    for redis_connection in redis_online:
        print(redis_connection['socket_id'])
        try:
            uo = UserOnline.objects.get(sid=redis_connection['socket_id'])
            uo.activity = time.time()
            uo.save()
        except Exception as e:
            print(e)
    
@task
def clear_from_online(data):
    set_user_offline(data)