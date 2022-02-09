from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from account.models import UserProfile
from account.user_serializer import ShortUserSerializer
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from .filters import SearchPersonFilter, SearchFeedFilter
from rest_framework.response import Response
from feed.serializers import ShortUserFeedSerializer, PostListSerializer
from feed.models import UserFeed


# Create your views here.

# class SearchTagView(APIView):
#     permission_classes = (AllowAny,)

#     def get(self, key):
#         # static_page = StaticPage.objects.filter(alias=alias).values('title', 'content').first()
#         return Response({'rezult': 'ok'})


class SearchTagView(generics.ListAPIView):
    serializer_class = ShortUserSerializer
    permission_classes = (AllowAny,)
    # pagination_class = LimitOffsetPagination

    # def get(self, request, *args, **kwargs):
    #     serializer = ShortUserSerializer(self.get_queryset(), many=True)
    #     page = self.paginate_queryset(serializer.data)
    #     return self.get_paginated_response(page)

    def get_queryset(self):
        """
           Search tags
        """
        keyw = self.kwargs['keyw']
        lstkw = keyw.split(',')
        print(keyw)
        return UserProfile.objects.filter(tags__name__in=lstkw)
        

# class SearchTagViewSet(viewsets.ModelViewSet):
#     serializer_class = ShortUserSerializer
#     queryset = UserProfile.objects.all()
#     filterset_fields = ['tags']
#     filter_class = SearchFilter

#     def get_queryset(self):
#         pr = self.request.user.userprofile
#         if pr.gender == 'female':
#             return UserProfile.objects.filter(gender='male')
#         else:
#             return UserProfile.objects.filter(gender='female')


class SearchTagPersonViewSet(viewsets.ModelViewSet):
    """
     Searching persons by tags divided by coma
    """
    serializer_class = ShortUserSerializer
    queryset = UserProfile.objects.all()
    filter_class = SearchPersonFilter
    filterset_fields = ['tags']
    permission_classes = (AllowAny,)
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        try:
            pr = self.request.user.userprofile
            if pr.gender == 'female':
                return UserProfile.objects.filter(gender='male')
            else:
                return UserProfile.objects.filter(gender='female')
        except:
            return UserProfile.objects.filter(gender='female')

class SearchTagFeedViewSet(viewsets.ModelViewSet):
    """
      Searching feeds by tags divided by coma
    """
    serializer_class = PostListSerializer
    queryset = UserFeed.objects.all().select_related('user')
    filter_class = SearchFeedFilter
    filterset_fields = ['tags']
    # pagination_class = LimitOffsetPagination

    def get_queryset(self):
        try:
            pr = self.request.user.userprofile
            if pr.gender == 'female':
                return UserFeed.objects.filter(user__gender='male')
            else:
                return UserFeed.objects.filter(user__gender='female')
        except:
            return UserFeed.objects.filter(user__gender='female')