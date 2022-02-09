from logsys.models import Log
from logsys.mixins.base import BaseLogMixin


class DatabaseLogMixin(BaseLogMixin):
    def log(self, username, ip_address, user_agent, log_type):
        return Log.objects.create(username=username, view_name=self.__class__.__name__, user_agent=user_agent,
                                  ip_address=ip_address, type=log_type)
