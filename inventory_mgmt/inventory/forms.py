from django import forms
from django.contrib.auth.models import User
from .models import trips, supplies, vans

class TripForm(forms.ModelForm):
    """This class will be used to build trips."""

    class Meta:
        """Specifying the database and fields to use."""

        model = trips
        fields = ['first_name', 'last_name', 'comments', 'payment_status', 'trip_start', 'trip_end', 'van_used', 'kayak_used', 'menu', 'extra_meals_purchased', 'extra_food_purchased', 'extra_supplies']


class SupplyForm(forms.ModelForm):
    """Allow the user to add a new item to the database."""

    class Meta:
        """Specify the db and fields that will be used."""

        model = supplies
        fields = ['supplyName', 'category', 'quantity', 'price']

class VanForm(forms.ModelForm):
    """Allow the user to add a new vehicle to the database."""

    class Meta:
        """Specify the db and fields that will be used."""

        model = vans
        fields = ['vanName', 'condition', 'available', 'mileage', 'trailer', 'comments']

class UserForm(forms.ModelForm):
    """This class will be used to make the form for account generation."""
    
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        """Specifying the database and fields to use."""
        
        model = User
        fields = ['username', 'email', 'password']