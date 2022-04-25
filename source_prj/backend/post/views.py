from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from account.models import UserProfile
from account.user_serializer import ShortUserSerializer
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from rest_framework.response import Response
from feed.serializers import ShortUserFeedSerializer, PostListSerializer
from feed.models import UserFeed


class PostListView(generics.ListAPIView):
    """
        Post list of another gender or female for guest
    """
    serializer_class = PostListSerializer
    permission_classes = (AllowAny,)
    # pagination_class = LimitOffsetPagination


    def get_queryset(self):
        try:
            profile = self.request.user.userprofile
            if profile.gender == 'male':
                return UserFeed.objects.filter(user__gender='female').select_related('user')
            else:
                return UserFeed.objects.filter(user__gender='male').select_related('user')
        except:
            return UserFeed.objects.filter(user__gender='female').select_related('user')
        