from django.shortcuts import render
from account.models import UserProfile, UserProfileDoc
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import exceptions
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from account.serializers import UserSerializer, UserProfileSerializer, ProfileCountrySerializer

from account.user_serializer import ShortUserSerializer
from django_countries.data import COUNTRIES
from django.utils.dateparse import parse_date
from props.models import Props, Value, Value2User
import base64
from django.core.files.base import ContentFile
import random
from account.moderation import moderate_new
from props.models import Props, Value2User, Value2User

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # todo rewrite, mb using raw sql
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            # with subquery
            # blocked = BlockList.objects.filter(block_by_user=self.request.user).values_list('profile')
            # queryset.objects.exclude(blocked_profiles__in=blocked)
            return queryset.raw(
                "SELECT account_userprofile.* FROM account_userprofile "
                "LEFT JOIN blocklist_blocklist "
                "ON (account_userprofile.user_ptr_id = blocklist_blocklist.profile_id AND"
                f" blocklist_blocklist.block_by_user_id={user_id}) "
                "WHERE blocklist_blocklist.profile_id IS NULL")
                # AND account_userprofile.user_ptr_id !={user_id}
        return queryset


class CheckEmail(APIView):
    """
       Initialization
    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        email = request.data.get("email")
        try:
            User.objects.get(email=email)
            print('Yes')
            return Response({'status': 1, 'message': 'Error!!!'})
        except:
            print('No!')
            return Response({'status': 0, 'message': 'Ok'})

        print(email)
        return Response({'status': 0, 'message': 'Ok'})


class ProfileDetailView(APIView):
    """
    Detail information of user account.views.profile ProfileDetailView.

    @param [1,2,3]

    """
    permission_classes = (AllowAny,)
    def post(self, request):
        print(request.data)
        out = {}
        try:
            cntx ={"user_id": request.user.userprofile.id}
        except:
            cntx = {}
        for user_id in request.data:
            out[user_id] = ShortUserSerializer(instance=UserProfile.objects.get(pk=user_id),context=cntx).data
        return Response(out)
        #profile = UserProfile.objects.get(pk=id)
        #return Response({ id: ShortUserSerializer(profile).data})


class ProfileCountryView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileCountrySerializer


class ProfileSaveBasicInfoView(APIView):
    """
      Saving Basic profile information
    """
    def post(self, request, format=None):
        profile = request.user.userprofile
        profile.publicname = request.data.get('username')
        profile.last_name = request.data.get('lastName')
        profile.birthday = parse_date('%s-%s-%s' % (request.data.get('birthday')['year'],request.data.get('birthday')['month'],request.data.get('birthday')['day']))
        profile.country = request.data.get('country')
        profile.city = request.data.get('city')
        profile.lookingfor = request.data.get('lookingfor')
        profile.about_me = request.data.get('about_me')

        profile.save()
        # print(request.data)
        # marrital status
        prop = Props.objects.get(alias='marital')
        v1 = Value.objects.get(prop=prop, name_en='Married')
        v2 = Value.objects.get(prop=prop, name_en='Single')
        Value2User.objects.filter(prop=prop,user=profile).delete()
        if(request.data.get('status') == 'Married'):
            p2u = Value2User.objects.create(prop=prop,user=profile,value=v1)
        else:
            p2u = Value2User.objects.create(prop=prop,user=profile,value=v2)
        
        return Response({"status": 0, "message": "Ok"})

class ProfileSaveDetailView(APIView):
    """
      Saving Detail profile information
    """
    def post(self, request, format=None):
        print(request.data)
        profile = request.user.userprofile
        Value2User.objects.filter(user=profile).delete()
        #Value2User.objects.all().delete()
        for key in request.data:
            try:
                print(request.data[key])
                prop = Props.objects.get(alias=key)
                value = Value.objects.get(id=request.data[key])
                Value2User.objects.create(user=profile, value=value, prop=prop)
            except Exception as e:
                print(e)
                print(key)
        profile.job = request.data.get('job')
        profile.goal = request.data.get('goal')
        profile.save()

        return Response({"status": 0, "message": "Ok"})



class ProfileSaveDocsView(APIView):
    """
      Saving verify documents
    """
    def post(self, request, format=None):
        profile = request.user.userprofile

        try:
             format, imgstr1 = request.data.get('passport').split(';base64,')
        except:
             return Response({"status": 1, "message": _('No! You need to donload passport!.')})

        try:
             format, imgstr2 = request.data.get('psychReport').split(';base64,')
        except:
             return Response({"status": 1, "message": _('No! You need to donload a psych report!.')})

       
        ext1 = format.split('/')[-1]
        data1 = ContentFile(base64.b64decode(imgstr1))
        file_name1 = '%s-%s.%s' % (profile.id,random.randint(111,999),ext1) 

        ext2 = format.split('/')[-1]
        data2 = ContentFile(base64.b64decode(imgstr2))
        file_name2 = '%s-%s.%s' % (profile.id,random.randint(111,999),ext2)

        d = UserProfileDoc()
        d.first_name = request.data.get('name')
        d.last_name = request.data.get('lastName')
        d.user = profile
        d.save()
        d.image1.save(file_name1, data1, save=True)
        d.image2.save(file_name2, data2, save=True)
        moderate_new(d)
        # print(request.data)
        return Response({"status": 0, "message": _('Thankyou, you documents hass been sent to the moderator.')})