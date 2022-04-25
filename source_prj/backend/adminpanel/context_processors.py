"""
    Context processor for collecting data from models to display on the main page
    Added to backend/settings.py -> TEMPLATES ->'OPTIONS' -> context_processors'
"""

from .modelworks.feed_work.feeduser import UserFeedWork

def appruve_data(request) -> dict:
    admin_data = dict()
    admin_data['feed_men_count'] = UserFeedWork.get_feedcount_men_noappruve()
    admin_data['feed_women_count'] = UserFeedWork.get_feedcount_woman_noappruve()

    return admin_data