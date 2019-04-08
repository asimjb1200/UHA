from django import forms
from django.contrib.auth.models import User
from .models import trips, customer, supplies, vans, kayak, meal, menu, food, menu_meals, MealItem

class TripForm(forms.ModelForm):
    """This class will be used to build trips."""

    class Meta:
        """Specifying the database and fields to use."""
        model = trips
        fields = ['first_name', 'last_name', 'comments', 'payment_status', 'trip_start', 'trip_end', 'van_used', 'kayak_used', 'menu', 'extra_meals_purchased', 'extra_food_purchased', 'extra_supplies']

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["van_used"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["van_used"].queryset = vans.objects.filter(available=True)
        self.fields["kayak_used"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["kayak_used"].queryset = kayak.objects.filter(available=True)
        self.fields["extra_meals_purchased"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["extra_food_purchased"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["extra_supplies"].widget = forms.widgets.CheckboxSelectMultiple()


class FoodForm(forms.ModelForm):
    class Meta:
        model = food
        fields = ['food_name', 'price', 'quantity', 'warehouse']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["warehouse"].widget = forms.widgets.CheckboxSelectMultiple()


class CustomerForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'group_size']

class MealForm(forms.ModelForm):
    class Meta:
        model = meal
        fields = ['meal_name', 'items', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['items'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["items"].queryset = food.objects.all()


class MenuForm(forms.ModelForm):
    class Meta:
        model = menu
        fields = ['menu_name', 'meal_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meal_name'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields['meal_name'].queryset = meal.objects.all()


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