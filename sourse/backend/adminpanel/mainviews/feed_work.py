"""
   Functional for working with feeds users
"""
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from feed.models import UserFeed
from .mainview import BaseAdminView
from adminpanel.modelworks.feed_work.feeduser import UserFeedWork

"""
   Get all mens feeds for moderate
"""
class GetManFeedForModerate(BaseAdminView, ListView):
    template_name = 'feeds/man_feed.html'
    context_object_name = 'feed_men'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(GetManFeedForModerate, self).get_context_data(**kwargs)
        context['tab_feed'] = True
        context['tab_feed_man'] = True
        return context

    def get_queryset(self):
        return UserFeedWork.get_all_men_no_appruved()


"""
   Get all womens feeds for moderate
"""
class GetWomanFeedForModerate(BaseAdminView,  ListView):
    template_name = 'feeds/woman_feed.html'
    context_object_name = 'feed_women'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(GetWomanFeedForModerate, self).get_context_data(**kwargs)
        context['tab_feed'] = True
        context['tab_feed_woman'] = True
        return context

    def get_queryset(self):
        return UserFeedWork.get_all_woman_no_appruved()


"""
    View single feed
"""
class ViewFeed(BaseAdminView, DetailView):
    model = UserFeed
    context_object_name = 'post'
    template_name = 'feeds/view_feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tab_feed'] = True
        context['tab_feed_woman'] = True
        context['tab_feed_man'] = True
        return context