from rest_framework import routers
from collections import OrderedDict

class RootRouter(routers.DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        #api_root_dict['url'] = 'tpl'

        return self.APIRootView.as_view(api_root_dict=api_root_dict)
