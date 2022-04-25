from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from account.user_serializer import user_serializer, ShortUserSerializer
from account.models import UserProfile
from props.models import Props, Value, Value2User
from usermedia.models import UserMedia
from usermedia.serializers import UserMediaPhotoSerializer
from django.utils.translation import ugettext_lazy as _
from feed.serializers import ShortUserFeedSerializer
from logsys.mixins.db_log import DatabaseLogMixin
from backend.settings import DOMAIN


# Create your views here.
class GalleryListView(APIView):
    """
       Get gallery
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            profile = request.user.userprofile
            if profile.gender == 'male':
                users = UserProfile.objects.filter(gender='female')
            else:
                users = UserProfile.objects.filter(gender='male')
            is_auth = True
        except:
            users = UserProfile.objects.filter(gender='female')
            is_auth = False

        try:
            if kwargs['online'] == 'true':
                users = users.filter(is_online=True)
        except:
            pass

        try:
            if kwargs['age_from'] != 'all':
                afrom = kwargs['age_from']
                # users = users.filter(birthday__gt=kwargs['age_from'])
                # print('aaaageeeeefrom')
            else:
                afrom = 'all'
        except Exception as e:
            afrom = 'all'

        try:
            if kwargs['age_to'] != 'all':
                ato = kwargs['age_to']
                # users = users.filter(birthday__lt=kwargs['age_from'])
                # print('aaaageeeeeto')
            else:
                ato = 'all'
        except:
            afrom = 'all'

        if (afrom != 'all' and ato == 'all'):
            users = users.filter(birthday__lt=afrom)

        if (ato != 'all' and afrom == 'all'):
            users = users.filter(birthday__gt=ato)

        if (afrom != 'all' and ato != 'all'):
            users = users.filter(birthday__lt=afrom, birthday__gt=ato)

        out = {
            'ids': [],
            'results': {}
        }
        for user in users:
            serialized_user = ShortUserSerializer(user).data
            if is_auth:
                serialized_user['is_subscribed'] = profile.check_subscription(user)
            try:
                serialized_user['last_feed'] = ShortUserFeedSerializer(user.getLastFeed()).data
            except:
                serialized_user['last_feed'] = {}
            out['ids'].append(user.id)
            out['results'][user.id] = serialized_user
        return Response(out)


class GalleryDetailView(DatabaseLogMixin, APIView):
    """
       Get gallery detail
    """
    permission_classes = (AllowAny,)
    log_type = 'detail_gallery'
    def get(self, request, id, format=None):
        out = {'props': [], 'gallery': []}
        profile = UserProfile.objects.get(pk=id)
        out['user'] = ShortUserSerializer(profile).data
        props = Props.objects.filter(for_woman=True)
        for p in props:
            try:
                v = Value2User.objects.get(user=profile, prop=p)
                value = v.value.name
                id = v.value.id
            except:
                value = 'none'
                id = 0 
            out['props'].append({'name': p.name, 'value': value, 'alias': p.alias, 'icon': DOMAIN+p.icon.url, 'id': id})
        gallery = UserMedia.objects.filter(user=profile, is_approved=True, is_main=False)
        for g in gallery:
            out['gallery'].append(UserMediaPhotoSerializer(g, context={'request': request}).data)
        # print(gallery)

        return Response(out)