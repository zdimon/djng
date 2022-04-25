import json

import redis
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError

from account.models import UserProfile
from feed.serializers import UserFeedSerializer
from account.user_serializer import ShortUserSerializer
from .serializers import LikeSerializer

from .models import Likes
from backend.settings import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)


class LikeItView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    def post(self, request, *args, **kwargs):
        obj_model = request.data.get('obj_model')
        obj_id = request.data.get('obj_id')
        try:
            model_class = ContentType.objects.get(model=obj_model).model_class()
            obj = model_class.objects.get(id=obj_id)
        except ContentType.DoesNotExist as e:
            response_data = {'status': 1,
                             'message': f'{obj_model} {_("model does not exist")}',
                             'details': f'{e}'
                             }
        except model_class.DoesNotExist as e:
            response_data = {'status': 1,
                             'message': f'{_("object with id does not exist")}',
                             'details': f'{e}'}
        else:
            user_profile = request.user.userprofile
            try:
                Likes.objects.create(content_object=obj, liker=user_profile)
                response_data = {'status': 0,
                                 'feed': UserFeedSerializer(obj).data,
                                 'message': _(
                                     f"user profile with id {user_profile.id} likes object {obj_model} with id {obj_id}")}

            except IntegrityError:
                response_data = {'status': 1, 'message': _('Error, duplicate record!')}
            else:
                dest_user = getattr(obj, 'user', None)
                if isinstance(dest_user, UserProfile):
                    for uo in dest_user.get_socket_ids():
                        data = {
                            'task': 'put_to_socket',
                            'data': {
                                'action': 'server-action:like_add',
                                'socket_id': uo.sid,
                                'data': {
                                    'post_id': obj_id,
                                    'user': ShortUserSerializer(user_profile).data,
                                    'created_at': '1999-01-01'
                                }
                            }
                        }
                        data['socket_id'] = uo.sid
                        redis_client.publish('notifications', json.dumps(data))

        return Response(response_data)
