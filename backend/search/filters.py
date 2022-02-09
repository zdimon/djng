from django_filters import FilterSet, DateTimeFilter, CharFilter
from account.models import UserProfile
from feed.models import UserFeed



from taggit.forms import TagField
from django_filters.views import FilterView

class TagFilter(CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, **kwargs)



class SearchPersonFilter(FilterSet):
    tags = TagFilter(field_name='tags__slug')
    
    class Meta:
        model = UserProfile
        fields = ['tags']

class SearchFeedFilter(FilterSet):
    tags = TagFilter(field_name='tags__slug')
    
    class Meta:
        model = UserFeed
        fields = ['tags']
