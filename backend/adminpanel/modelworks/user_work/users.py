"""
    Functional for working with a model User, UserProfile for users on th site
"""
from account.models import UserProfile
from django.contrib.auth.models import User

class UserProfileWork:

    @staticmethod
    def get_men_data():
        return UserProfile.objects.filter(gender="male").only('id', 'title', 'is_stories', 'created_at')

    @staticmethod
    def get_woman_data():
        return UserProfile.objects.filter(gender="female").only('id', 'title', 'is_stories', 'created_at')

class UserWork:
    pass