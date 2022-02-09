"""
   Functional for working with users on the site
"""
from account.models import UserProfile
from django.views.generic.detail import DetailView
from .mainview import BaseAdminView

"""
    View Single User profile
"""
class ViewUserProfile(BaseAdminView, DetailView):
    model = UserProfile
    context_object_name = 'user'
    template_name = 'users/user_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tab_feed'] = True
        context['tab_feed_woman'] = True
        context['tab_feed_man'] = True
        return context