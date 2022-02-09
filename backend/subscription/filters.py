from django_filters import FilterSet, CharFilter, NumberFilter
from subscription.models import BonusSubscription2PaymentType


class BonusSubsFilter(FilterSet):
    id = NumberFilter(field_name='bonus_subscription__id', lookup_expr='exact')
    alias = CharFilter(field_name='payment_type__alias', lookup_expr='exact')


    class Meta:
        model = BonusSubscription2PaymentType
        fields = ['id', 'alias']
