from grappelli.dashboard import modules, Dashboard


class WebmasterAdminDashboard(Dashboard):
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.children.append(modules.ModelList(
            column=1,
            collapsible=False,
            # css_classes=("grp-closed",),
            models=('webmaster.models.*',),
        ))
