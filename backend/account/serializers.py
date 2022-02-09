from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import UserProfile
from rest_framework import serializers
from django_countries.data import COUNTRIES


class UserSerializer(serializers.ModelSerializer):
    is_edit = serializers.SerializerMethodField('is_edit_func')
    
    def is_edit_func(self, foo):
        return False

    class Meta:
        model = UserProfile
        fields = ['id', 'url', 'account', 'username', 'email', 'groups', 'is_superuser', 'is_edit', 'main_photo',
                  'is_online']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'about_me',
            'publicname',
            'lastname',
            'birthday',
            'lookingfor',
            'goal',
            'job',
            'city',
            'country'

        ]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordTokenSerializer(serializers.Serializer):
    password = serializers.CharField(label=_('Password'), style={'input_type': 'password'})
    token = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class ProfileCountrySerializer(serializers.ModelSerializer):
    code = serializers.CharField(source='country')

    class Meta:
        model = UserProfile
        fields = 'id', 'code'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.update({'name': COUNTRIES[representation['code']]})
        return representation
