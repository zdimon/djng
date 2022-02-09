"""
    ClientSocket - client socket class for testing server socket
"""
import sys
import socketio
import json
from testwogs.testsdir.classes.http_client import Client as Cl
from testwogs.testsdir.classes.log_manager import LogManager
#for run from clear console python client_socket.py
# from backend.backend.testwogs.testsdir.classes.log_manager import LogManager

class ClientSocket:
    client = Cl()
    sio = socketio.Client()
    log_manager = LogManager()

    def __init__(self):
        self.sio = socketio.Client()



    @staticmethod
    @sio.event
    def disconnect():
        print('disconnected from server')
        #sio.disconnect()
        # sys.exit()

    @staticmethod
    @sio.on('notifications')
    def on_message(data):
        print('I received a message!')
        print(data)

    @staticmethod
    def run_server():
        ClientSocket.sio.connect('http://localhost:8889/websocket/', socketio_path="/websocket")
        # ClientSocket.sio.emit('sid', {'EIO': 3, 'transport': 'websocket', 'sid': ClientSocket.sio.sid})
        #ClientSocket.sio.wait()

# @sio.event
# def my_message(data):
#     print('message received with ', data)
    
#     def connect(self,token, account):
#         try:
#             self.sio.connect('http://localhost:8889/websocket/', socketio_path="/websocket")
#         except:
#             LogManager.server_error()
#         data_request = {'token': token, 'socket_id': self.sio.sid}
#         print(data_request)
#         print(account)
#         rec = self.client.post_json('http://localhost:8085/online/update/socket/id', data_request, token)
#         ClientSocket.log_manager.add(rec.status_code, '/online/update/socket/id',
#                                          json.dumps(data_request), rec.text, alias='socket_test')
#         # ClientSocket.sio.emit('sid', {'EIO': 3, 'transport': 'websocket', 'sid': ClientSocket.sio.sid})
#         self.sio.wait()   

if __name__ == '__main__':
    siO = ClientSocket()
    siO.run_server()
