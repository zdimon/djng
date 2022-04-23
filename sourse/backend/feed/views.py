import redis
from django.shortcuts import render

from django.core.exceptions import ImproperlyConfigured
from account.serializers import UserSerializer
from usermedia.models import UserMedia
from .serializers import UserFeedSerializer, UserFeedCommentSerializer
from .models import UserFeed, UserFeedComment
from account.models import UserProfile
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.base import ContentFile
import base64
import json
from .tasks import take_pic_from_video
import random
from moderation.utils.feed import moderate_new_feed
from django.contrib.gis.geoip2 import GeoIP2
from core.iputils import get_client_ip
from django.utils.translation import ugettext_lazy as _
from feed.models import UserFeedSubscription
from account.user_serializer import ShortUserSerializer
from chat.models import ChatContact
from backend.settings import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)

# Create your views here.
class FeedViewSet(viewsets.ModelViewSet):
    """
    API endpoint for feed.
    """
    queryset = UserFeed.objects.filter(is_approved=True)
    serializer_class = UserFeedSerializer

    def get_queryset(self):
        user = self.request.user.userprofile
        subscriptions = [subscription.get('user_destination') for subscription in UserFeedSubscription.objects.filter(user_subscriber = user).values('user_destination')]
        favorites = [abonent.get('abonent') for abonent in ChatContact.objects.filter(owner=user).values('abonent')]
        favoriteFeeds = UserFeed.objects.filter(user__in=favorites, is_approved=True) 
        return UserFeed.objects.filter(user=user).order_by('-id')
        # return favoriteFeeds.union(UserFeed.objects.filter(user__in=subscriptions, is_approved=True), UserFeed.objects.filter(user=user, is_approved=True), all=True)


    def perform_create(self, serializer):
        feed = serializer.save()
        # take_pic(video)


class UserFeedDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserFeedSerializer
    queryset = UserFeed.objects.all().order_by('-id')  


class FeedOfUserView(ListAPIView):
    serializer_class = UserFeedSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        # print(user_id)
        user = UserProfile.objects.get(pk=user_id)
        return UserFeed.objects.filter(is_approved=True, user=user).order_by('-id')


class UserFeedSaveView(APIView):
    '''

    Saving feed.

    '''

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        pr = request.user.userprofile
        ip = get_client_ip(request)
        print('ip - %s' % ip)
        ip = '193.151.241.65'
        geo = GeoIP2()
        c = geo.city(ip)
        print(c)
        # print(request.data['id'])

        if request.data['id'] != 'null':
            uf = UserFeed.objects.get(pk=request.data['id'])
        else:
            uf = UserFeed()
            uf.user = pr
        uf.lon = str(c['longitude'])
        uf.lat = str(c['latitude'])
        uf.city = str(c['city'])
        uf.country = str(c['country_name'])
        uf.is_approved = False
        uf.title = request.data['title']
        uf.text = request.data['text']
        uf.save()
        # print(request.data['images'])
        imgdata = json.loads(request.data['images'])
        cam_imgdata = json.loads(request.data['cam_images'])

        # video from comp
        for v in request.data.getlist('video[]'):
            p = UserMedia()
            p.feed = uf
            p.type_media = 'video'
            p.video.save('tmpvid.mp4', v, save=True)
            p.save()
            take_pic_from_video(p)

        # video from cam
        for v in request.data.getlist('cam_video[]'):
            p = UserMedia()
            p.feed = uf
            p.type_media = 'video'
            p.video.save('camvid.mp4', v, save=True)
            p.save()
            take_pic_from_video(p)

        if imgdata != 'undefined':
            for im in imgdata:
                format, imgstr = im['data'].split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr))
                file_name = '%s-%s.%s' % (uf.id, im['name'], ext)
                p = UserMedia()
                p.feed = uf
                p.type_media = 'photo'
                p.image.save(file_name, data, save=True)
                p.save()
        # print(request.data['cam_images'])

        for im in cam_imgdata:
            format, imgstr = im['imgBase64'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            file_name = '%s-%s.%s' % (uf.id, random.randint(111, 999), ext)
            p = UserMedia()
            p.feed = uf
            p.type_media = 'photo'
            p.image.save(file_name, data, save=True)
            p.save()

        moderate_new_feed(uf)
        return Response(UserFeedSerializer(uf).data)


class FeedSubscribeView(APIView):
    """
       Subscribe user on feed
       @param id: number
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        subscriber = request.user.userprofile
        destination = UserProfile.objects.get(pk=id)
        try:
            UserFeedSubscription.objects.get(user_subscriber=subscriber, user_destination=destination)
            mes = {'status': 1, 'message': _('You already subscribed!'), 'user_id': id}
        except:
            UserFeedSubscription.objects.create(user_subscriber=subscriber, user_destination=destination)
            mes = {'status': 0, 'message': _('You have been subscribed!'), 'user_id': id}
        return Response(mes)

class FeedUnsubscribeView(APIView):
    """
       Unsubscribe user from feed
       @param id: number
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, format=None):
        subscriber = request.user.userprofile
        destination = UserProfile.objects.get(pk=id)
        try:
            s = UserFeedSubscription.objects.get(user_subscriber=subscriber, user_destination=destination)
            s.delete()
            mes = {'status': 0, 'message': _('You have been unsubscribed!'), 'user_id': id}
        except:
            UserFeedSubscription.objects.create(user_subscriber=subscriber, user_destination=destination)
            mes = {'status': 1, 'message': _('Error!'), 'user_id': id}
        return Response(mes)

class UserFeedSubscriberListView(APIView):
    """
       List of subscribers
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user.userprofile
        subscribers = UserFeedSubscription.objects.filter(user_subscriber=user)
        out = {'ids': [], 'rezults': {}, 'list': []}
        for s in subscribers:
            suser = ShortUserSerializer(s.user_destination).data
            out['ids'].append(s.user_destination.id)
            out['list'].append(suser)
            out[s.user_destination.id] = suser
        return Response(out)


class UserFeedCommentView(ListCreateAPIView):
    queryset = UserFeedComment.objects.all()
    model = UserFeedComment
    serializer_class = UserFeedCommentSerializer

    def perform_create(self, serializer):
        comment_feed = get_object_or_404(UserFeed, id=self.request.data.get('feed'))
        return serializer.save(feed=comment_feed)


class UserFeedCommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = UserFeedComment.objects.all()
    model = UserFeedComment
    serializer_class = UserFeedCommentSerializer

class FeedAddNewView(APIView):
    """
      Saving feed from my profile
    """
    def post(self, request, format=None):
        profile = request.user.userprofile
        feed = UserFeed()
        feed.user = profile
        feed.title = request.data['title']
        # feed.is_approved = True
        feed.text = request.data['description']
        # feed.is_stories = request.data['is_stories']
        # print(request.data.get('is_stories'))
        if request.data.get('is_stories') == 'true':
            feed.is_stories = True
        else:
            feed.is_stories = False
        feed.save()
        mcollect = []
        for i in [1,2,3,4]:
            try:
                v = request.data.get('video'+str(i))
                if v:
                    p = UserMedia()
                    p.feed = feed
                    p.type_media = 'video'
                    p.user = profile
                    p.video.save('camvid%s.mp4' % str(i), v, save=True)
                    p.save()
                    take_pic_from_video(p)   
                    mcollect.append(p)
            except Exception as e:
                print(e)
            try:
                imgstr = request.data.get('image'+str(i))
                if imgstr:
                    format, imgstr = imgstr.split(';base64,')
                    ext = format.split('/')[-1]
                    data = ContentFile(base64.b64decode(imgstr))
                    file_name = '%s-%s.%s' % (feed.id, i, ext)
                    p = UserMedia()
                    p.feed = feed
                    p.type_media = 'photo'
                    p.user = profile
                    p.image.save(file_name, data, save=True)
                    p.save()
                    mcollect.append(p)
            except Exception as e:
                print(e)
        # TODO сделать не рандомно а пропустить главное с формы
        try:
            rnd = random.randint(0,len(mcollect)-1)
        except:
            rnd = 0
        feed.last_media = mcollect[rnd]
        feed.save()

        # хуячим на модерацию
        moderate_new_feed(feed)

        #######################################################

        # сохраняем теги
        tlist = request.data.get('tags').split(',')
        for t in tlist:
            feed.tags.add(t)

        try:
            it = mcollect[rnd]
            it.is_main = True
            it.save()
        except:
            return Response({'status': 1, 'message': 'Error on saving FeedAddNewView'})


        #print(request.data)
        return Response({'status': 0, 'message': 'Ok'})

class FeedRemoveView(APIView):
    """
      Removing feed post
    """
    def get(self, request, post_id, format=None):
        profile = request.user.userprofile
        post = UserFeed.objects.get(pk=post_id)
        if post.user == profile:
            post.delete()
        return Response({'status': 0, 'message': 'Ok'})

class FeedCommentAddView(APIView):
    """
      Add feed comment.
      Send socket message.
    """
    def post(self, request, format=None):
        profile = request.user.userprofile
        print(request.data)
        post = UserFeed.objects.get(pk=request.data.get('id'))
        comment = UserFeedComment()
        comment.user = profile
        comment.feed = post
        comment.text = request.data.get('comment')
        comment.save()

        target_profile = post.user
        if target_profile != profile:
            for online in target_profile.get_socket_ids():
                data = {
                    'task': 'put_to_socket',
                    'data': {
                        'action': 'server-action:comment_add',
                        'socket_id': online.sid,
                        'data': {
                            'id': comment.id,
                            'post_id': post.id,
                            'commentator': ShortUserSerializer(profile).data,
                            'text': comment.text,
                            'created': str(comment.created_at)
                        }
                    }
                }
                redis_client.publish('notifications', json.dumps(data))
        #post.delete()
        return Response({'status': 0, 'message': _('Message has been saved!'), 'comment': UserFeedCommentSerializer(comment).data})


class FeedCommentsInfoView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        feed = UserFeed.objects.get(pk=id)
        users_comment = UserFeedComment.objects.filter(feed=feed).exclude(user=feed.user).values('user').order_by().distinct()
        data = {}
        for user_id in users_comment:
            user = UserProfile.objects.get(pk=user_id.get('user'))
            last_feed = user.getLastFeed()
            count_user_feeds = UserFeed.objects.filter(user=user).count()

            last_feed_serializer = UserFeedSerializer(last_feed)
            user_serializer = UserSerializer(user, context={'request': request})

            data[user.id] = {'user': user_serializer.data,
                             'last_feed': last_feed_serializer.data,
                             'count_user_feeds': count_user_feeds
                             }

        return Response({'status': 0,
                         'message': 'Ok',
                         'data': data,
                         })

class ThrowError(APIView):
    def get(self, request):
        raise ImproperlyConfigured
        return Response({'status': 1,
                         'message': 'Error',
                         'data': data,
                         })
