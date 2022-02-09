from rest_framework import serializers

from .models import BonusSubscription2PaymentType, BonusSubscriptionUsedLog


class BonusSubscriptionLimitsSerializer(serializers.ModelSerializer):
    alias = serializers.CharField(source='payment_type.alias', read_only=True)
    expire = serializers.CharField(source='bonus_subscription.expire_at', read_only=True)

    class Meta:
        model = BonusSubscription2PaymentType
        fields = 'id', 'alias', 'limit', 'limit_units', 'expire'
        extra_kwargs = {
            'limit_units': {'read_only': True},
        }

    def validate(self, attrs):
        if not attrs.get('limit'):
            raise serializers.ValidationError({'limit': ['This field is required']})
        if attrs.get('limit') <= 0:
            raise serializers.ValidationError({'limit': ['Limit must be positive']})
        return attrs

    def update(self, instance, validated_data):
        how_much = validated_data.pop('limit')
        if instance.limit == 0 or (instance.limit - how_much) < 0:
            raise serializers.ValidationError({'limit': ['limit is exceeded']})
        instance.limit -= how_much
        BonusSubscriptionUsedLog.objects.create(user=self.context['request'].user.userprofile, how_much=how_much,
                                                used_service=instance)
        return super().update(instance, validated_data)
