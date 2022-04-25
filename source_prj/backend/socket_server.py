#!/usr/bin/env python
import tornado.ioloop
import tornado.web
from tornado import autoreload
import socketio
import json
from tornado.ioloop import IOLoop
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from django.contrib.auth.models import User
from online.models import UserOnline
from account.models import UserProfile
import aioredis
import asyncio
import requests
from backend.settings import DOMAIN
from online.tasks import clear_from_online
from tornado import gen
DEBUG_MODE = True
from backend.local import SSL_KEYS
# clear tables
UserOnline.objects.all().delete()
for user in UserProfile.objects.filter(is_online=True):
    user.set_offline()

mgr = socketio.AsyncRedisManager('redis://localhost:6379/0')
#mgr = socketio.RedisManager('redis://')
sio = socketio.AsyncServer(async_mode='tornado', logger=True, cors_allowed_origins=[
    'http://localhost:4545',
    'http://localhost:4200',
    'http://localhost'],client_manager=mgr)
sio.current_connections = []
CELERY_CONFIG_MODULE='backend.celery'

import redis
redis_client = redis.Redis(host='localhost', port=6379, db=4)

@gen.coroutine
def small_loop():
    while True:
        yield print('\nin small loop!\n')
        yield gen.sleep(10)


async def consumer(channel):
    '''
        Messages from REDIS (notifications chanel)
        {
            'task': '<task-name>',
            'data': '<payload>'
        }

        if task == put_to_socket

        {
            'task': 'put_to_socket',
            'data': {
                'socket_id': '<socket_id>'
                'action': '<action_name>'
            }
        }

    '''
    while await channel[0].wait_message():
        msg = await channel[0].get()
        data = json.loads(msg.decode("utf-8"))
        print('Message from redis %s' %  data['task'])
        #print(data)
        if data['task'] == 'put_to_socket':
            payload = {
                'data': data['data']
            }
            print('sending to %s action: %s' % (data['data']['socket_id'], data['data']['action']))
            await sio.emit(data['data']['action'], payload, room=data['data']['socket_id'])
        if data['task'] == 'gather_active_connections':
            print('getting active connections')
            sio.current_connections = [] 
            redis_client.set('socket_connections',json.dumps(sio.current_connections))
            payload = {'message': 'give me your fucking sid plz!'}
            await sio.emit('server-action:ping', payload)

        if data['task'] == 'user_offline' or data['task'] == 'user_online' or data['task'] == 'update_user':
            print('Sending notification about updating of/online')
            #print(data)
            await sio.emit('server-action:update_user_online',data)

        if data['task'] == 'send_chat_message_to_sids':
            # print('send_chat_message_to_sids')
            for sid in data['sids']:
                print('send_chat_message_to_sids: %s ' % sid)
                payload = {
                    'data': data
                    }
                await sio.emit('server-action:chat_message',payload, room=sid)
        #if
        #await sio.emit('server-action:user_online', {'users': [1,2,3]})
        #for connection in connections:
        #    await connection.write_message(msg)


async def setup():
    print('Setup')
    connection = await aioredis.create_redis('redis://localhost:6379/0')
    channel = await connection.subscribe('notifications')
    #print(channel)
    asyncio.ensure_future(consumer(channel))


@sio.event
def connect(sid, environ):
    print("connect ", sid)



@sio.on('ng-action')
async def chat_message(sid, data):
    '''
        Messages from Angular
    '''
    print("ACTION: %s" % data['action'])
    if DEBUG_MODE:
        print("message ", data)
    if data['action'] == 'pong':
        print('Pong')
        sio.current_connections.append({'socket_id':data['socket_id'],'token': data['token']})
        redis_client.set('socket_connections',json.dumps(sio.current_connections))
    if data['action'] == 'get_active_connections':
        await sio.emit('active-connections',sio.current_connections,room=sid)


    #if data['action'] == 'MESSAGE:set_me_online' or data['action'] == 'MESSAGE:set_me_offline':
    #    await sio.emit('server-action:update_user_online', data)

    # server-action:user_online emitting
    #await sio.emit('server-action:user_online', {'users': [1,2,3]})
    
    #users_online.append(data['username'])
    #redis_client.set('users_online',json.dumps(users_online))
   
    #await UserOnline.set_online(data['username'],sid)
    #await sio.save_session(sid, {'username': data['username']})
    #session = await sio.get_session(sid)
    #print(session['username'])

    
@sio.event
async def disconnect(sid):
    print('disconnectinggg ', sid)
    #url = '%s/celery/task' % DOMAIN
    data = {'socket_id': sid}
    #redis_client.publish('notification', json.dumps(data))
    #res = await requests.post(url,data=data)    
    #await sio.emit('server-action:update_user_online')
    clear_from_online.delay(data)


def make_app():
    return tornado.web.Application([
        (r"/websocket/", socketio.get_tornado_handler(sio)),
    ])
    
'''

app.listen(args.listen_port, args.listen_interface, ssl_options={ 
        "certfile": os.path.join(lib_dir, "mydomain.crt"),
        "keyfile": os.path.join(lib_dir, "mydomain.key"),
    })

'''
from backend.local import IS_SSL_SERVER
if __name__ == "__main__":
    print('Starting server on 8889 port')
    autoreload.start()
    autoreload.watch('socket_server.py')
    app = make_app()
    '''
        Certificate Path: /etc/letsencrypt/live/dating-test.webmonstr.com/fullchain.pem
        Private Key Path: /etc/letsencrypt/live/dating-test.webmonstr.com/privkey.pem
    '''


    if IS_SSL_SERVER:
        app.listen(8889,ssl_options=SSL_KEYS)
    else:
        app.listen(8889)

    '''
        if IS_SSL_SERVER:
            app.listen(8889,ssl_options={ 
                "certfile": '/home/webmaster/fullchain1.pem',
                "keyfile": '/home/webmaster/privkey1.pem',
            })
        else:
            app.listen(8889)
    '''
    
    loop = IOLoop.current()
    loop.add_callback(setup)
    #loop.instance().spawn_callback(small_loop)
    loop.start()
