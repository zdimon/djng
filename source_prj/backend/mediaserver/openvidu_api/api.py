import requests
import base64
import json
from django.conf import settings

address = settings.OPENVIDU_SERVER_URL
token = str(base64.b64encode(bytes(settings.OPENVIDU_SERVER_SECRET, 'utf-8')), 'utf-8')


# todo add logging?

class OpenVidu:
    headers = {'Authorization': f'Basic {token}', 'Content-Type': 'application/json'}

    def init_session(self, params=None, token=None):
        path = '/sessions'
        headers = self.headers
        if token:
            headers = self._update_headers({'Authorization': f'Basic {token}'})

        return self.hit_api('post', path, headers, params)

    def generate_token(self, params):
        path = '/tokens'
        return self.hit_api('post', path, self.headers, params)

    def retrieve_active_sessions(self, session_id=None):
        if not session_id:
            session_id = ''
        path = f'/sessions/{session_id}'
        return self.hit_api('get', path, self._update_headers({'Content-Type': 'application/x-www-form-urlencoded'}))

    def close_session(self, session_id):
        path = f'/sessions/{session_id}'
        return self.hit_api('delete', path, self._update_headers({'Content-Type': 'application/x-www-form-urlencoded'}))

    @staticmethod
    def hit_api(method, path, headers, data=None):
        url = f'{address}/api{path}'
        if data:
            data = json.dumps(data)
        try:
            response = getattr(requests, method)(url, headers=headers, data=data)
        except requests.exceptions.ConnectTimeout as e:
            response_data = {'error': f'{e}'}
        else:
            if response.status_code not in (502, 503, 409, 429, 521):
                response_data = json.loads(response.content)
            else:
                response_data = {'error': response.status_code}
        return response_data

    def _update_headers(self, h):
        common_headers = self.headers.copy()
        common_headers.update(h)
        return common_headers
