import django_filters
from .models import supplies, customer, food

class SupplyFilter(django_filters.FilterSet):
    """Specifying what I want the user to be able to filter the data set for."""
 
    class Meta:
        model = supplies
        fields = {
            'supplyName': ['icontains'],
            'category': ['icontains'],
        }


class CustomerFilter(django_filters.FilterSet):
    """Allow the user to search for a specific customer."""

    class Meta:
        model = customer
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
        }

class FoodFilter(django_filters.FilterSet):
    """Specifying what I want the user to be able to filter the data set for."""
 
    class Meta:
        model = food
        fields = {
            'food_name': ['icontains'],
            'warehouse__location': ['icontains'],
        }