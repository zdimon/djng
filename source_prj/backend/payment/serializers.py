from rest_framework import serializers
from .models import Payment, PaymentType, Agency2Woman2PaymentType
from account.serializers import UserProfileSerializer
from account.user_serializer import ShortUserSerializer
from agency.serializers import AgencySerializer


class PaymentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    reciver = ShortUserSerializer()
    class Meta:
        model = Payment
        fields = ['id', 'type', 'ammount', 'payer', 'reciver', 'created_at']
        # depth = 2
    def get_type(self,obj):
        return obj.type.name


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'alias', 'price', 'name', 'procent_for_agency']
        # depth = 2


class Agency2Woman2PaymentTypeSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer()
    woman = UserProfileSerializer(read_only=True)
    agency = AgencySerializer(read_only=True)

    class Meta:
        model = Agency2Woman2PaymentType
        fields = 'agency', 'woman', 'payment_type', 'commission'
