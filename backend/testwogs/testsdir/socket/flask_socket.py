import socketio
import json
import sys
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('ng-action',{'action': 'get_active_connections'})

@sio.on('active-connections')
def on_message(data):
    print('I received a message!')
    print(data)

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect('http://localhost:8888',socketio_path="/websocket")
