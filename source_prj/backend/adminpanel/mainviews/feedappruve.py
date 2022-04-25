"""
   Moderation of posts and their media content
"""
from .mainview import BaseAdminView
from django.shortcuts import redirect
from adminpanel.modelworks.feed_work.feeduser import UserFeedWork

"""
   Appruved post
"""
class AppruveFeed(BaseAdminView):
    def get(self, request, *args, **kwargs):
        data = UserFeedWork.approuve_post(kwargs['pk'])
        if data and kwargs['gender'] == 'men':
            redirect_url = 'getmenfeed'
            return redirect(redirect_url)
        else:
            redirect_url = 'getwomanfeed'
            return redirect(redirect_url)