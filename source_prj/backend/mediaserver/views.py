from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .openvidu_api.api import OpenVidu
from rest_framework.permissions import IsAuthenticated
from logsys.mixins.db_log import DatabaseLogMixin

ov = OpenVidu()


class OpenViduView(DatabaseLogMixin, viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def init_session(self, request):
        self.log_type = 'ov_init_session'
        data = self.request.data
        print(data)
        response = ov.init_session(data)
        return Response(response)

    def get_token(self, request):
        """session argument is required"""
        self.log_type = 'ov_get_token'
        data = self.request.data
        response = ov.generate_token(data)
        return Response(response)

    def get_active_sessions(self, request, session_id=None):
        self.log_type = 'ov_get_active_sessions'
        response = ov.retrieve_active_sessions(session_id)
        return Response(response)

    def close_session(self, request, session_id):
        self.log_type = 'ov_close_sessions'
        response = ov.close_session(session_id)
        return Response(response)
