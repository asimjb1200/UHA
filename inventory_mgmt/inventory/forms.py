from django import forms
from django.contrib.auth.models import User
from .models import tripItinerary, trips, warehouse, trailers, customer, supplies, vans, kayak, meal, menu, food, van_kit, VanKitMasterlist #menu_meals, MealItem,
# from .models import tripItinerary, itineraryDays
from django.forms import ModelForm, modelformset_factory, inlineformset_factory, formset_factory

# class tripsform(forms.ModelForm):
#     class Meta:
#         model = trips
#         exclude = ('comments', 'payment_status', 'trip_start', 'trip_end', 'van_used', 'kayak_used', 'menu', 'extra_food_purchased', 'extra_meals_purchased', 'extra_supplies')

class itineraryform(forms.ModelForm):
    class Meta:
        model = tripItinerary
        #exclude = ('tripItinerary', )
        fields = ['Itinerary_title', 'itinerary']
        #fields = ['name']
    
# ItineraryFormSet = inlineformset_factory(tripItinerary, itineraryDays, 
#     fields=['arrival','dropoff','activities'],
#     form=itineraryform, extra=1)
#         #ItineraryFormSet = formset_factory(itineraryform, extra=1)
#         #ItineraryFormSet = modelformset_factory(tripItinerary, extra=1, fields=['arrival','dropoff','activities',])


class TripForm(forms.ModelForm):
    """This class will be used to build trips."""

    class Meta:
        """Specifying the database and fields to use."""
        model = trips
        fields = ['first_name', 'last_name','comments', 'payment_status', 'trip_start', 'trip_end',
                  'van_used', 'kayak_used', 'menu', 'extra_meals_purchased', 'extra_supplies', 'trip_Itinerary']

        widgets = {
            'first_name': forms.Textarea(attrs={'placeholder': "Enter primary contact's first name here", 'rows':1}),
            'last_name': forms.Textarea(attrs={'placeholder': "Enter primary contact's last name here", 'rows':1}),
            'comments': forms.Textarea(attrs={'placeholder': 'Place any extra comments here', 'rows':8}),
            'trip_start': forms.DateInput(attrs={'placeholder': "Start date. Format: mm/dd/yyyy"}),
            'trip_end': forms.DateInput(attrs={'placeholder': "End date. Format: mm/dd/yyyy"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["van_used"].queryset = vans.objects.filter(available=True)
        self.fields["kayak_used"].queryset = kayak.objects.filter(available=True)
        self.fields["extra_supplies"].queryset = supplies.objects.all()
        self.fields["trip_Itinerary"].queryset = tripItinerary.objects.all()
    

class FoodForm(forms.ModelForm):
    class Meta:
        model = food
        fields = ['food_name', 'price', 'quantity', 'warehouse']

        widgets = {
            'food_name': forms.Textarea(attrs={'placeholder': "Enter name of item", 'rows':1}),
            'price': forms.NumberInput(attrs={'placeholder': "Enter price per unit", 'rows':1}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter item quantity', 'rows':1}),
            }
        

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = warehouse
        fields = ['location']


class KayakForm(forms.ModelForm):
    class Meta:
        model = kayak
        fields = ['kayak_name', 'warehouse', 'condition', 'available']

        widgets = {
            'kayak_name': forms.Textarea(attrs={'placeholder': "Enter the name of the kayak", 'rows':1}),
        }


class TrailerForm(forms.ModelForm):
    class Meta:
        model = trailers
        fields = ['trailer_name', 'warehouse', 'condition', 'available']

        widgets = {
            'trailer_name': forms.Textarea(attrs={'placeholder': "Enter the name of the trailer", 'rows':1}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['first_name', 'last_name',
                  'phone_number', 'email', 'group_size']
        
        widgets = {
            'first_name': forms.Textarea(attrs={'placeholder': "Enter customer's first name", 'rows':1}),
            'last_name': forms.Textarea(attrs={'placeholder': "Enter customer's last name", 'rows':1}),
            'email': forms.EmailInput(attrs={'placeholder': "Enter customer's email address", 'rows':1}),
            'group_size': forms.NumberInput(attrs={'placeholder': "Enter the customer's group size", 'rows':1}),
        }


class MealForm(forms.ModelForm):
    class Meta:
        model = meal
        fields = ['meal_name', 'items', 'description']

        widgets = {
            'meal_name': forms.Textarea(attrs={'placeholder': "Enter the name of the meal", 'rows':1}),
            'description': forms.Textarea(attrs={'placeholder': "Place any important information about the meal here", 'rows':8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["items"].queryset = food.objects.all()


class MenuForm(forms.ModelForm):
    class Meta:
        model = menu
        fields = ['menu_name', 'meal_name']

        widgets = {
            'menu_name': forms.Textarea(attrs={'placeholder': "Enter the menu's name here", 'rows':1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meal_name'].queryset = meal.objects.all()


class SupplyForm(forms.ModelForm):
    """Allow the user to add a new item to the database."""

    class Meta:
        """Specify the db and fields that will be used."""

        model = supplies
        fields = ['supplyName', 'category', 'quantity', 'price']

        widgets = {
            'supplyName': forms.Textarea(attrs={'placeholder': "Enter the item's name", "rows":1}),
            'price': forms.NumberInput(attrs={'placeholder': "Enter price per unit", 'rows':1}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter item quantity', 'rows':1}),

        }


class VanForm(forms.ModelForm):
    """Allow the user to add a new vehicle to the database."""

    class Meta:
        """Specify the db and fields that will be used."""

        model = vans
        fields = ['vanName', 'condition', 'available',
                  'mileage', 'trailer', 'comments']

        widgets = {
            'vanName': forms.Textarea(attrs={'placeholder': "Enter the vehicle's name", "rows":1}),
            'mileage': forms.NumberInput(attrs={'placeholder': "Enter the vehicle's current mileage", "rows":1}),
            'comments': forms.Textarea(attrs={'placeholder': "Enterh any pertinent information about the vehicle here", "rows":8})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trailer'].queryset = trailers.objects.filter(available=True)


class UserForm(forms.ModelForm):
    """This class will be used to make the form for account generation."""

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """Specifying the database and fields to use."""

        model = User
        fields = ['username', 'email', 'password']


class VanKitForm(forms.ModelForm):
    """Allow the user to add a new vk to the database."""

    class Meta:
        """Specify the db and fields that will be used."""

        model = van_kit
        fields = ['van_kit_name', 'vanName', 'Available', 'comments']

        widgets = {
            'van_kit_name': forms.Textarea(attrs={'placeholder': "Enter the van kit's name", "rows":1}),
            'comments': forms.Textarea(attrs={'placeholder': "Enter any pertinent information about the vehicle here", "rows":8})
        }


class VKMasterlistForm(forms.ModelForm):
    """Allow the user to add a new item to the database."""

    class Meta:
        """Specify the db and fields that will be used."""

        model = VanKitMasterlist
        fields = ['supplyName', 'supplyQuantity']

        widgets = {
            'supplyName': forms.Textarea(attrs={'placeholder': "Enter the item's name", "rows":1}),
            'supplyQuantity': forms.NumberInput(attrs={'placeholder': 'Enter item quantity', 'rows':1}),
        }