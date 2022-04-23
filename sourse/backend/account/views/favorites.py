from rest_framework.views import APIView
from rest_framework.response import Response
from payment.tasks import update_account_service
from chat.models import ChatContact
from account.models import UserProfile
from account.user_serializer import ShortUserSerializer
from rest_framework import generics
from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    abonent = ShortUserSerializer()
    id = serializers.CharField()


    def create(self, validated_data):
        return {'message': ok}

class FavoriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatContact 
        fields = ['abonent', 'id']   

class FavoritesView(generics.ListAPIView):
    '''
    Favorites list of the user by taken token. 

    @header: user token

    '''
    queryset = ChatContact.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        pr = self.request.user.userprofile
        return ChatContact.objects.filter(owner=pr)
