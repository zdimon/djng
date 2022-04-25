from django.contrib.auth.models import Group
from rest_framework import generics, pagination
from account.serializers.group import GroupSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User


class UserGroupListView(generics.ListAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    filterset_fields = ['id', 'name']
    pagination_class = pagination.LimitOffsetPagination

'''
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = User.objects.get(pk=request.GET.get('user_id'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
'''