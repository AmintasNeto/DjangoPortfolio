import django_filters
from django_filters import DateFilter,CharFilter
from .models import *


class OrderFilter(django_filters.FilterSet):
    startDate = DateFilter(field_name='dateCreated', lookup_expr='gte')
    endDate = DateFilter(field_name='dateCreated', lookup_expr='lte')
    notes = CharFilter(field_name='notes', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'dateCreated']
