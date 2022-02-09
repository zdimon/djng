from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from account.user_serializer import user_serializer
from account.models import UserProfile
from payment.models import Payment, PaymentType
from props.models import Props, Value, Value2User
from payment.serializers import PaymentSerializer
from rest_framework import pagination
from collections import OrderedDict
from rest_framework.generics import ListAPIView

from subscription.filters import BonusSubsFilter
from subscription.models import BonusSubscription2PaymentType, BonusSubscription
from subscription.serializers import BonusSubscriptionLimitsSerializer
from payment.utils import process_transaction

class PaymentFilterListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        receiver = request.user.userprofile
        payments = Payment.objects.filter(reciver_id=receiver.id)

        out = {
            'ids': [],
            'results': {}
        }
        for payment in payments:
            out['ids'].append(payments[0].payer_id)
            out['results'][payments[0].payer_id] = user_serializer(payments[0].payer)

        return Response(out)


class PaymentListView(ListAPIView):
    '''
        List of users payments.
    '''
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(payer=self.request.user.userprofile).order_by('-id')





class PaymentServicesView(UpdateModelMixin, APIView):
    permission_classes = (IsAuthenticated,)

    """
        {'service_type':'sticker', 'limit':1, 'room_id': 23}
        limit - here, how much was used
    """

    def post(self, request, *args, **kwargs):
        up = self.request.user.userprofile
        
        if (up.gender == 'female'):
            return Response({'message': 'Ok', 'status': 0})

        self.q = BonusSubscription.objects.filter(replenishmentlog__user_profile=up)
        last = self.q.last()

        # use bonus_subscription and it limits for services
        if last and last.is_active():
            try:
                su_pu = super().partial_update(request, *args, **kwargs)
            except KeyError:
                return Response({'service_type': 'this field is required', 'status': 1})
            su_pu.data.update({'status': 0})
            data = su_pu.data
        # use user's account
        else:
            service_type = PaymentType.objects.get(alias=self.request.data['service_type'])
            if (up.account - service_type.price) < 0:
                return Response({'message': 'insufficient funds', 'status': 2})
            payment = process_transaction(up,service_type,request.data)
            data = {'message': 'No subscription or service limit exceeded. Amount paid from account', 
                    'status': 0, 
                    'account': up.account, 
                    'payment_id': payment.id
                    }
        return Response(data)

    """
        all bellow need for UpdateModelMixin
    """
    def get_queryset(self):
        return self.q.last().services.all()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), payment_type__alias=self.request.data['service_type'])

    def get_serializer(self, *args, **kwargs):
        return BonusSubscriptionLimitsSerializer(*args, **kwargs, context={'request': self.request})
