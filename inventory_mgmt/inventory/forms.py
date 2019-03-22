from django import forms
from .models import trips
from .models import van_kit

class TripForm(forms.ModelForm):
    class Meta:
        model = trips
        fields = ['first_name', 'last_name', 'comments', 'payment_status', 'trip_start', 'trip_end', 'van_used', 'kayak_used', 'menu', 'extra_meals_purchased', 'extra_food_purchased', 'extra_supplies']


class VanKitForm(forms.ModelForm):
    class Meta:
        model = van_kit
        fields = ['supply_name', 'van_kit_name', 'vanName', 'Available', 'comments']

