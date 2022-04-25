from django_filters import FilterSet, DateTimeFilter, CharFilter, BooleanFilter
from django.contrib.auth.models import User


class UserFilter(FilterSet):
    username = CharFilter(field_name='username', lookup_expr='icontains')
    email = CharFilter(field_name='email', lookup_expr='icontains')
    is_superuser = BooleanFilter(field_name='is_superuser')
    is_staff = BooleanFilter(field_name='is_staff')
    is_active = BooleanFilter(field_name='is_active')
     
    class Meta:
        model = User
        fields = ['username', 'email', 'is_superuser', 'is_staff', 'is_active']
