from django.http import Http404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import BonusSubsFilter
from .serializers import BonusSubscriptionLimitsSerializer
from .models import BonusSubscription2PaymentType


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = BonusSubscription2PaymentType.objects.all()
    serializer_class = BonusSubscriptionLimitsSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = BonusSubsFilter

    def get_queryset(self):
        self.queryset = BonusSubscription2PaymentType.objects.filter(
            bonus_subscription__replenishmentlog__user_profile=self.request.user.userprofile)
        return super().get_queryset()

    """
        {"id":43, "limit":1}
        id - BonusSubscription2PaymentType obj id, 
        limit - here, how much was used
    """

    def partial_update(self, request, *args, **kwargs):
        try:
            su_pu = super().partial_update(request, *args, **kwargs)
        except KeyError:
            return Response({'id': 'this field is required', 'status': 1})
        data = su_pu.data
        data.update({'status': 0})
        return Response(data=data)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=self.request.data['id'])

