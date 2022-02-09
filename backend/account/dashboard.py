from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name

from backend.dashboard import CommonDashboard


class SuperAdminDashboard(CommonDashboard):

    def __init__(self, **kwargs):
        CommonDashboard.__init__(self, **kwargs)
        self.children.append(modules.ModelList(
            title='Users',
            column=2,
            collapsible=True,
            # css_classes=("grp-closed",),
            models=('account.models.UserProfile',),
        ))

        self.children.append(modules.AppList(
            title='Users online',
            column=5,
            collapsible=True,
            # css_classes=("grp-closed",),
            models=('usermedia.models.*',),
        ))
        self.children.append(modules.ModelList(
            title=_('Applications'),
            column=1,
            collapsible=True,
            exclude=('django.contrib.auth.models.Group',),
        ))
        #
        self.children.append(modules.AppList(
            title=_('User media'),
            column=2,
            collapsible=False,
            # css_classes=("grp-closed",),
            models=('usermedia.models.*', ),
        ))

        self.children.append(modules.AppList(
            title=_('Feed media'),
            column=2,
            collapsible=False,
            # css_classes=("grp-closed",),
            models=('feed.models.*', ),
        ))
        # append an app list module for "Administration"

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.AppList(
            title='test',
            column=3,
            collapsible=False,
            # css_classes=("grp-closed",),
            models=('account.models.*',),
        ))
        self.children.append(modules.AppList(
            title='test',
            column=3,
            collapsible=False,
            # css_classes=("grp-closed",),
            models=('online.models.*',),
        ))

    #     self.children.append(modules.Group(
    #         _(u'Управление сайтом и приложениями'),
    #         column=1,
    #         collapsible=True,
    #         # css_classes=("grp-closed",),
    #         children = [
    #             modules.AppList(
    #                 _(u'Администрирование'),
    #                 column=1,
    #                 collapsible=False,
    #                 models=('administration.models.*',),
    #             ),
    #             modules.AppList(
    #                 _(u'Приложения'),
    #                 column=1,
    #                 css_classes=('collapse closed',),
    #                 exclude=('django.contrib.*',),
    #             )
    #         ]
    #     ))
