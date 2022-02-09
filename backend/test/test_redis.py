import socketio
import json
#external_sio = socketio.RedisManager('redis://', write_only=True, channel='notifications')
data = json.dumps({'foo': 'barrrrrrrr'})
#external_sio.emit('ng-action:set_online', data=data)
import sys
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

from datetime import datetime
startTime = datetime.now()

for i in range(0,10000):
    data = json.dumps({'foo': i})
    redis_client.publish('notifications', data)


print(datetime.now() - startTime)

sys.exit()

import socketio

# asyncio
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect('http://localhost:8888',socketio_path="/websocket")

from datetime import datetime
startTime = datetime.now()

for i in range(0,10000):
    #data = json.dumps({'foo': i})
    #redis_client.publish('notifications', data)
    sio.emit('ng-action:set_online', data={'username': i})

print(datetime.now() - startTime)