from django_filters import FilterSet, DateTimeFilter, CharFilter
from logsys.models import Log


class LogsFilter(FilterSet):
    date_to = DateTimeFilter(field_name='created_at', lookup_expr='lte')
    date_from = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    ip_address = CharFilter(field_name='ip_address', lookup_expr='contains')
    username = CharFilter(field_name='username', lookup_expr='contains')
    type = CharFilter(field_name='type', lookup_expr='iexact')

    class Meta:
        model = Log
        fields = ['date_from', 'date_to', 'ip_address', 'username', 'type']
