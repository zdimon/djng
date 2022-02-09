import socketio
from testwogs.testdir.classes.http_client import Client

sio = socketio.Client()
http = Client()
@sio.event
def connect():
    print('connection established')
    print(sio.sid)

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:8889/' , socketio_path="/websocket")
sio.wait()
if __name__ == '__main__':
    loop.run_until_complete(start_server())