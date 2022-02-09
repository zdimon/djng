"""
    ClientSocket - client socket class for testing server socket
"""
import sys
import socketio
import json
from testwogs.testsdir.classes.http_client import Client as Cl
from testwogs.testsdir.classes.log_manager import LogManager
#for run from clear console python client_socket.py
# from backend.backend.testwogs.testsdir.classes.http_client import Client as Cl
# from backend.backend.testwogs.testsdir.classes.log_manager import LogManager

class ClientSocket:
    client = Cl()
    sio = socketio.Client()
    log_manager = LogManager()

    @staticmethod
    @sio.event
    def connect():
        print(3000)
        print('connection established', ClientSocket.sio.sid)
        data_request = {'token': 'b284331d0fc911cc218ecaac9910648c73d5c2ae', 'socket_id': ClientSocket.sio.sid}
        rec = ClientSocket.client.post_json('http://localhost:8085/online/update/socket/id', data_request)
        if rec.status_code == 200:
            # truncate data, save data in DB
            ClientSocket.log_manager.truncate_db()
            ClientSocket.log_manager.add(rec.status_code, '/online/update/socket/id',
                                         json.dumps(data_request), rec.text, alias='socket_test')

            # information output to the console
            print('=' * 50)
            print(f'URL_REQUEST - "/online/update/socket/id"\nSockettest completion status - {rec.status_code} - Ok')
            print('=' * 50)
            ClientSocket.disconnect()
        else:
            # truncate data, save data in DB
            ClientSocket.log_manager.truncate_db()
            ClientSocket.log_manager.add(rec.status_code, "/online/update/socket/id", test_status='no successfully',
                                         api_status=1, alias='login')
            # information output to the console
            print('=' * 50)
            print(f'Something is wrong.\nURL_REQUEST - "/online/update/socket/id"\nTest completion status - {rec.status_code}')
            print('=' * 50)
            ClientSocket.disconnect()

    @staticmethod
    @sio.event
    def disconnect():
        print('disconnected from server')
        #sio.disconnect()
        # sys.exit()

    @staticmethod
    @sio.on('my message')
    def on_message(data):
        print('I received a message!')
        print(data)

    @staticmethod
    def run_server():
        ClientSocket.sio.connect('http://localhost:8889/websocket/', socketio_path="/websocket")
        # ClientSocket.sio.emit('sid', {'EIO': 3, 'transport': 'websocket', 'sid': ClientSocket.sio.sid})
        ClientSocket.sio.wait()


if __name__ == '__main__':
    siO = ClientSocket()
    siO.run_server()
