from usermedia.models import UserMedia
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from payment.utils import check_media_meassage_payment, check_user_account_meassage_payment, process_transaction_with_message_obj
from chat.models import ChatMessage
from usermedia.serializers import UserMediaPhotoSerializer, UserMediaVideoSerializer

class ChangeRoleMediaView(APIView):
    '''
        Changing role of the media
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user.userprofile
        photo = UserMedia.objects.get(pk=request.data['photo']['id'])
        if photo.user == user:
            photo.role_media = request.data['value']
            photo.save()
        return Response({'status': 0, 'message': _('Photo was changed.')})

class GetPrivateMediaView(APIView):
    '''
        Get info about access to private media
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user.userprofile
        # print(request.data)
        message = ChatMessage.objects.get(pk = request.data['message_id'])
        # photo = UserMedia.objects.get(pk=request.data['media_id'])
        # if photo.user == user:
        #     photo.role_media = request.data['value']
        #     photo.save()
        rez = check_media_meassage_payment(message, request)
        return Response(rez)

class PayPrivateMediaView(APIView):
    '''
        Get info about access to private media
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user.userprofile
        # print(request.data)
        message = ChatMessage.objects.get(pk = request.data['message_id'])
        # photo = UserMedia.objects.get(pk=request.data['media_id'])
        # if photo.user == user:
        #     photo.role_media = request.data['value']
        #     photo.save()
        #rez = check_media_meassage_payment(message)
        process_transaction_with_message_obj(user, message)
        if not check_user_account_meassage_payment(message, user):
            return Response({'status': 2, 'message': _('No money!')})
        obj = message.content_object
        if obj.type_media == 'video':
            serializer = UserMediaVideoSerializer
        if obj.type_media == 'photo':
            serializer = UserMediaPhotoSerializer
        media = serializer(message.content_object).data
        return Response({'status': 0, 'message': _('Good.'), 'media': media, 'account': user.account})