import base64
import random
from django.contrib.auth.models import User

from account.serializers import UserSerializer
from .models import UserMedia
from rest_framework import serializers
from moderation.utils.photo import moderate_new
from django.core.files.base import ContentFile

from .utils import recalc_crop_coordinates

class UserMediaPhotoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMedia
        fields = [
            'id',
            'is_main',
            'get_small_url_square',
            'role_media',
        ]

class UserMediaPhotoSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    img_pos = serializers.JSONField(write_only=True, required=False)
    crop_pos = serializers.JSONField(write_only=True, required=False)

    # get_image may be triggered one more time,(ex. access to self.data inside create)
    _image = None

    class Meta:
        model = UserMedia
        fields = [
            'id', 'type_media', 'role_media', 'user', 'image', 'video', 'is_main',
            'is_approved', 'is_deleted', 'type_media', 'role_media', 'price', 'geolocation',
            'croppos_land', 'croppos_port', 'croppos_square', 'get_small_url_port', 'get_middle_url_port',
            'get_small_url_land', 'get_middle_url_land', 'get_small_url_square',
            'get_middle_url_square', 'image_big', 'get_video_url', 'img_pos', 'crop_pos', 'get_url_blur'
        ]

    def get_user(self, obj=None):
        if obj:
            return obj.user.id
        return self.context.get('request').user.userprofile.id

    # w = UserSerializer(self.context['request'].user.userprofile, context=self.context)

    def get_image(self, obj=None):
        request = self.context.get('request')
        if obj:
            return obj.image.url
        elif request:
            if self._image:
                return self._image
            elif type(request.data.get('image')) is str:
                format_part, base64_image = request.data.get('image').split(';base64,')
                ext = format_part.split('/')[-1]
                imgdata = base64.b64decode(base64_image)
            else:
                ext = request.data.get("image").name.split('.')[-1]
                imgdata = request.data.get('image').read()
            file_name = f'{random.randint(111, 999)}.{ext}'
            self._image = ContentFile(imgdata, file_name)
            return self._image

    def create(self, validated_data):
        data = {
            'image': self.get_image(),
            'user': self.context['request'].user.userprofile,
            'type_media': 'photo',

        }
        if 'img_pos' in validated_data:
            img_pos = validated_data.pop('img_pos')
            port_coords = recalc_crop_coordinates('port', img_pos)
            land_coords = recalc_crop_coordinates('land', img_pos)
            square_coords = recalc_crop_coordinates(None, img_pos)
            data.update(cropping_port=port_coords, cropping_land=land_coords, cropping_square=square_coords)
        if 'crop_pos' in validated_data:
            crop_pos = validated_data.pop('crop_pos')
            port_coords = recalc_crop_coordinates('port', crop_pos)
            land_coords = recalc_crop_coordinates('land', crop_pos)
            square_coords = recalc_crop_coordinates(None, crop_pos)
            data.update(croppos_port=port_coords, croppos_land=land_coords, croppos_square=square_coords)

        data.update(validated_data)
        instance = super().create(data)
        moderate_new(instance)
        return instance


class UserMediaVideoSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return UserMedia.objects.create(**validated_data)

    class Meta:
        model = UserMedia
        fields = [
            'id',
            'user',
            'video',
            'image',
            'image_big',
            'is_deleted',
            'is_approved',
            'get_video_url',
            'is_main',
            'get_small_url_land',
            'get_middle_url_land',
            'type_media',
            'role_media',
        ]
