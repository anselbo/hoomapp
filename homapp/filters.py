import django_filters 
from django_filters import DateFilter, DateFromToRangeFilter
from .models import Wear, WearCategory

class WearFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains')
    # start_date = DateFilter(field_name='date_created', label='start date', lookup_expr='gte')
    # end_date = DateFilter(field_name='date_created', label='end date', lookup_expr='lte')
    date = DateFromToRangeFilter(field_name='date_created', label='Date')
    
    class Meta:
        model = Wear  
        fields = '__all__'
        exclude = ['user', 'photo', 'description', 'date_created', 'name',
                    'date_updated', 'amount', 'date_bought', 'bought_from', 'activate']