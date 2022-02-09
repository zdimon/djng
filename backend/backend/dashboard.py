from grappelli.dashboard import modules, Dashboard


class CommonDashboard(Dashboard):
    classes = ['SuperAdminDashboard', 'AgencyDashboard']

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        if self.__class__.__name__ in self.classes:
            """
                can be add common models, apps...
            """
            self.children.append(modules.AppList(
                column=1,
                collapsible=False,
                # css_classes=("grp-closed",),
                models=('account.models.*'),
            ))
