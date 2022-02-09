from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name

from backend.dashboard import CommonDashboard


class AgencyDashboard(CommonDashboard):

    def __init__(self, **kwargs):
        CommonDashboard.__init__(self, **kwargs)
        self.children.append(modules.AppList(
            column=1,
            collapsible=True,
            # css_classes=("grp-closed",),
            models=('agency.models.*',),
        ))
