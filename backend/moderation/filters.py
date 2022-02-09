from django_filters import FilterSet, DateTimeFilter, CharFilter
from moderation.models import Moderation


class ModerationFilter(FilterSet):
    type_obj = CharFilter(field_name='type_obj', lookup_expr='iexact')
    
    class Meta:
        model = Moderation
        fields = ['type_obj']
