from django.contrib.contenttypes.models import ContentType

from usermedia.models import UserMedia
from feed.models import UserFeed, UserFeedComment
from rest_framework import serializers
from account.user_serializer import ShortUserSerializer
from likes.models import Likes
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

class UserFeedCommentSerializer(serializers.ModelSerializer):
    # user = ShortUserSerializer()

    def create(self, validated_data):
        comment = UserFeedComment.objects.create(user=self.context['request'].user.userprofile, **validated_data)
        return comment

    class Meta:
        model = UserFeedComment
        fields = 'id', 'feed', 'text', 'user', 'parent_id', 'tree_id', 'level', 'lft', 'rght'


def user_feed_serializer(profile):
    from account.user_serializer import user_serializer

    data = {
        "id": profile.id,
        "feed": ShortUserFeedSerializer(profile.feed).data,
        "text": profile.text,
        "user": user_serializer(profile.user),
        "parent_id": profile.parent_id,
        "tree_id": profile.tree_id,
        "level": profile.level,
        "lft": profile.lft,
        "rght": profile.rght,
    }
    return data


class ShortUserMediaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    type_media = serializers.CharField(required=True)
    orient = serializers.CharField(required=True)
    middle_main_image_url = serializers.CharField(required=True)
    duration = serializers.CharField(required=False)
    # image = serializers.CharField(required=True)
    # main_media = UserFeedMediaSerializer()


class UserMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMedia
        fields = [
            'id',
            'type_media',

            'get_small_url_port',
            'get_middle_url_port',

            'get_small_url_land',
            'get_middle_url_land',

            'get_small_url_square',
            'get_middle_url_square',
            'get_url_blur',
            'image_big',
            'get_video_url',
            'orient',
            'role_media'

        ]


class UserFeedSerializer(serializers.ModelSerializer):
    # feedmedia = UserFeedMediaSerializer(many=True)
    feedcomment = UserFeedCommentSerializer(many=True)
    videos = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    # user = ShortUserSerializer()
    # likes = serializers.SerializerMethodField()

    def get_photos(self, obj):
        out = []
        for it in UserMedia.objects.filter(feed=obj, type_media="photo"):
            out.append(UserMediaSerializer(it).data)
        return out

    def get_videos(self, obj):
        out = []
        for it in UserMedia.objects.filter(feed=obj, type_media="video"):
            out.append(UserMediaSerializer(it).data)
        return out

    # def get_likes(self, obj):
    #     userfeed_type = ContentType.objects.get_for_model(UserFeed)
    #     return Likes.objects.filter(content_type__pk=userfeed_type.id, object_id=obj.id).count()

    class Meta:
        model = UserFeed
        fields = [
            'id',
            'title',
            'text',
            'user',
            'is_approved',
            'is_deleted',
            'has_video',
            'feedcomment',
            'videos',
            'photos',
            'lon',
            'lat',
            'city',
            'country',
            'likes',
            'created_at',
            'is_stories',
            'tags'

        ]




class ShortUserFeedSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True)
    location = serializers.CharField(required=True)
    likes = serializers.CharField(required=True)
    # image = serializers.CharField(required=True)
    main_media = ShortUserMediaSerializer()
    created_at = serializers.DateTimeField(format="%d-%m-%Y")
    count_photo = serializers.SerializerMethodField()
    count_video = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    #duration = serializers.CharField(required=True)

    """
           Return count user media in feed
    """
    def get_count_photo(self, obj) -> int:
        return obj.cnt_photo

    def get_count_video(self, obj) -> int:
        return obj.cnt_video

class PostListSerializer(ShortUserFeedSerializer): 
    user_id = serializers.CharField(required=True)
    main_media = ShortUserMediaSerializer()