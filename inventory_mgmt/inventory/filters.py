import django_filters
from .models import supplies

class SupplyFilter(django_filters.FilterSet):
    """Specifying what I want the user to be able to filter the data set for."""
 
    class Meta:
        model = supplies
        fields = {
            'supplyName': ['icontains'],
            'category': ['icontains'],
        }