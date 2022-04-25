"""
    Functional for working with a model UserFeed
"""
from feed.models import UserFeed
from adminpanel.modelworks.user_work.users import UserProfileWork

class UserFeedWork:

    @staticmethod
    def get_feedcount_men_noappruve():
        return UserFeed.objects.filter(is_approved=False).filter(user__in=UserProfileWork.get_men_data()).count()

    @staticmethod
    def get_feedcount_woman_noappruve():
        return UserFeed.objects.filter(is_approved=False).filter(user__in=UserProfileWork.get_woman_data()).count()

    @staticmethod
    def get_all_men_no_appruved():
        return UserFeed.objects.filter(is_approved=False).filter(user__in=UserProfileWork.get_men_data())

    @staticmethod
    def get_all_woman_no_appruved():
        return UserFeed.objects.filter(is_approved=False).filter(user__in=UserProfileWork.get_woman_data())

    @staticmethod
    def approuve_post(feed_id):
        return UserFeed.objects.filter(id=feed_id).update(is_approved=True)