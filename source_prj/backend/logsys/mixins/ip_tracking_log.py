from django.contrib.gis.geoip2 import GeoIP2

from .db_log import DatabaseLogMixin, Log
from .base import BaseLogMixin

from account.models import LoginWarningHistory
from account.models import UserProfile


class IpTrackingLog(DatabaseLogMixin, BaseLogMixin):
    def log(self, *arg, **kwargs):
        username = kwargs['username']
        previous_login_log = Log.objects.filter(username=username).values('ip_address').last()
        current_login_log = super().log(*arg, **kwargs)
        if previous_login_log and previous_login_log['ip_address'] != current_login_log.ip_address:
            previous_ip = previous_login_log['ip_address']
            current_ip = current_login_log.ip_address
            g = GeoIP2()
            prev_country = g.country(previous_ip)
            curr_country = g.country(current_ip)
            if prev_country['country_code'] != curr_country['country_code']:
                profile_id = UserProfile.objects.get(username=username).id

                LoginWarningHistory.objects.create(user_id=profile_id, current_warning_ip_address=current_ip,
                                                   previous_ok_ip_address=previous_ip, current_country=curr_country)
              
