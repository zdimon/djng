
from rest_framework import serializers


def user_serializer(profile):
    from feed.serializers import ShortUserFeedSerializer

    data = {}
    try:
        data = {
            "id": profile.id,
            "account": str(profile.account),
            "language": profile.language,
            "gender": profile.gender,
            "username": profile.publicname,
            "email": profile.email,
            "groups": [],
            "is_superuser": profile.is_superuser,
            "main_photo": profile.main_photo,
            "middle_photo": profile.middle_photo,
            "is_online": profile.is_online,
            "is_camera": profile.is_camera,
            "token": profile.get_token(),
            "last_feed": ShortUserFeedSerializer(profile.getLastFeed()).data
        }
    except Exception as ex:
        print(ex)
    return data


class ShortUserSerializer(serializers.Serializer):
    country_string = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(source='publicname')
    last_name = serializers.CharField()
    main_photo = serializers.CharField()
    age = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()
    language = serializers.CharField()
    is_online = serializers.BooleanField()
    about_me = serializers.CharField()
    account = serializers.CharField()
    lookingfor = serializers.CharField()
    is_camera = serializers.BooleanField()
    birthday = serializers.DateField()
    gender = serializers.CharField()
    is_verified = serializers.BooleanField()
    goal = serializers.CharField()
    job = serializers.CharField()
    zodiac = serializers.CharField()
    get_token = serializers.CharField()
    has_stories = serializers.SerializerMethodField()
    count_media = serializers.SerializerMethodField()
    is_online = serializers.BooleanField()

    def get_country_string(self,obj):
        return obj.get_country_display()

    def get_is_subscribed(self,obj):
        from account.models import UserProfile
        user_id = self.context.get("user_id")
        if user_id:
            user = UserProfile.objects.get(pk=user_id)
            print(user)
            return user.check_subscription(obj)
        else:
            return False
    """
        Check is user have posts as stories(feedmodel is_stories=True)
    """
    def get_has_stories(self, obj):
        is_feed = obj.userfeed_set.filter(is_stories=True).count()
        if is_feed:
            return True
        else:
            return False

    """
           Return count user media
    """
    def get_count_media(self, obj) -> int:
        return obj.usermedia_set.filter(user=obj).count()




class UserListItemSerializer(serializers.Serializer):
    country_string = serializers.SerializerMethodField()
    main_photo = serializers.SerializerMethodField()
    middle_photo = serializers.CharField()
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(source='publicname')
    last_name = serializers.CharField()
    main_photo = serializers.CharField()
    age = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()
    language = serializers.CharField()
    is_online = serializers.BooleanField()
    about_me = serializers.CharField()
    is_subscribed = serializers.SerializerMethodField()
    is_verified = serializers.BooleanField()

    def get_country_string(self,obj):
        return obj.get_country_display()

    def get_main_photo(self,obj):
        return obj.middle_photo()

    def get_is_subscribed(self,obj):
        return obj.check_subscription(obj)