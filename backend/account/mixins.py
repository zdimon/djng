from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache

from django.conf import settings


def check(request, path, groups):
    if request.user.is_authenticated and not request.user.is_superuser and request.path != path and request.user.groups.filter(
            name__in=groups):
        return True


class DashboardRedirectMixin:
    agency_path = '/agency/'
    moderator_path = '/moderator/'
    webmaster_path = '/webmaster/'

    """
        groups
    """
    ROLES = settings.SITE_GROUPS_ROLE

    @never_cache
    def index(self, request, extra_context=None):
        if check(request, path=self.agency_path, groups=self.ROLES['agency']):
            return HttpResponseRedirect(self.agency_path)
        elif check(request, path=self.moderator_path, groups=self.ROLES['moderator']):
            return HttpResponseRedirect(self.moderator_path)
        elif check(request, path=self.webmaster_path, groups=self.ROLES['webmaster']):
            return HttpResponseRedirect(self.webmaster_path)
        return super().index(request, extra_context=extra_context)
