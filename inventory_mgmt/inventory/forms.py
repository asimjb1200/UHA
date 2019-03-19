from django import forms
from django.contrib.auth.models import User
from .models import trips

class TripForm(forms.ModelForm):
    """This class will be used to build trips."""

    class Meta:
        """Specifying the database and fields to use."""

        model = trips
        fields = ['first_name', 'last_name', 'comments', 'payment_status', 'trip_start', 'trip_end', 'van_used', 'kayak_used', 'menu', 'extra_meals_purchased', 'extra_food_purchased', 'extra_supplies']


class UserForm(forms.ModelForm):
    """This class will be used to make the form for account generation."""
    
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        """Specifying the database and fields to use."""
        
        model = User
        fields = ['username', 'email', 'password']