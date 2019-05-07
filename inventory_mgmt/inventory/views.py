from django.views import generic
from django.shortcuts import render, redirect
from .models import supplies, van_kit, vans, trips, meal, menu, food, customer, warehouse, trailers, kayak, VanKitMasterlist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .filters import SupplyFilter, CustomerFilter
from .forms import SupplyForm, WarehouseForm, KayakForm, TrailerForm, FoodForm, CustomerForm, MenuForm, UserForm, TripForm, VanForm, MealForm, VanKitForm, VKMasterlistForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import ItineraryFormSet, tripsform, itineraryform
from django.db import transaction
from django.views.generic import ListView
from .models import tripItinerary

@login_required
def index(request):
    """Display the landing page of the website."""
    return render(request, 'inventory/index.html')


class ItineraryList(ListView):
    model = trips
    template_name = 'inventory/view-itinerary.html'
    success_url = reverse_lazy('index')
    fields = ['first_name', 'last_name']

class createItinerary(CreateView):
    model = tripItinerary
    #fields = ['first_name']
    template_name = 'inventory/itinerary-form.html'
    form_class = itineraryform

    def get_context_data(self, **kwargs):
        data = super(createItinerary, self).get_context_data(**kwargs)
        if self.request.POST:
            data['familymembers'] = ItineraryFormSet(self.request.POST)
        else:
            data['familymembers'] = ItineraryFormSet()
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()

                #if familymembers is not None:
                #    return redirect('inventory:index')
                
        return super(createItinerary, self).form_valid(form)


    

class ItineraryUpdate(UpdateView):
    model = trips
    template_name = 'inventory/itinerary-form.html'
    form_class = itineraryform
    success_url = reverse_lazy('viewitinerary')

    def get_context_data(self, **kwargs):
        data = super(ItineraryUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['familymembers'] = ItineraryFormSet(self.request.POST, instance=self.object)
        else:
            data['familymembers'] = ItineraryFormSet(instance=self.object)
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()

                #if familymembers is not None:
                #    return redirect('inventory:viewitinerary')
                
        return super(ItineraryUpdate, self).form_valid(form)


class Customers(LoginRequiredMixin, generic.ListView):
    model = customer
    template_name = 'inventory/customers.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        """Return a list of all customers."""
        return customer.objects.all()

    def get_context_data(self, **kwargs):
        # get the context data from the generic list view
        context = super().get_context_data(**kwargs)
        # add the filter to the context that will go to the template
        context['filter'] = CustomerFilter(self.request.GET, queryset=self.get_queryset())
        return context


class OtherCompanyInfo(LoginRequiredMixin, generic.ListView):
    model = warehouse
    template_name = 'inventory/warehouses.html'
    login_url = '/'
    redirect_field_name ='redirect_to'
    def get_queryset(self):
        return warehouse.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['trailer_list'] = trailers.objects.all()
        context['kayak_list'] = kayak.objects.all()
        return context


class CustomerUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    """This view will allow the user to update customer information."""

    model = customer
    form_class = CustomerForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:customers')


class NewTrailer(LoginRequiredMixin, View, PermissionRequiredMixin):
    """This view will allow the user to add a trailer"""
    
    form_class = TrailerForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            trailer = form.save(commit=False) 

            trailer_name = form.cleaned_data['trailer_name']
            warehouse = form.cleaned_data['warehouse']
            condition = form.cleaned_data['condition']
            available = form.cleaned_data['available']

            trailer.save()

            if trailer is not None:
                return redirect('inventory:other')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})


class TrailerUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    """This view will allow the user to update customer information."""

    model = trailers
    form_class = TrailerForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:other')


class NewKayak(LoginRequiredMixin, View, PermissionRequiredMixin):
    """This view will allow the user to add a kayak to the database."""
    
    form_class = KayakForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            kayak = form.save(commit=False) 

            kayak_name = form.cleaned_data['kayak_name']
            warehouse = form.cleaned_data['warehouse']
            condition = form.cleaned_data['condition']
            available = form.cleaned_data['available']

            kayak.save()

            if kayak is not None:
                return redirect('inventory:other')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})


class KayakUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    """This view will allow the user to update meals."""

    model = kayak
    form_class = KayakForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:other')


class NewWarehouse(LoginRequiredMixin, View, PermissionRequiredMixin):
    """This view will allow the user to add a warehouse to the database."""
    
    form_class = WarehouseForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            storage = form.save(commit=False) 

            location = form.cleaned_data['location']

            storage.save()

            if storage is not None:
                return redirect('inventory:other')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})



class NewCustomer(LoginRequiredMixin, View, PermissionRequiredMixin):
    """This view will allow the user to add a customer to the database."""
    
    form_class = CustomerForm
    template_name = 'inventory/new-customer.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            newCust = form.save(commit=False) 

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            group_size = form.cleaned_data['group_size']

            newCust.save()

            if newCust is not None:
                return redirect('inventory:customers')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})


class MealsView(LoginRequiredMixin, generic.ListView):
    """Display menus and meals to the user"""

    model = meal
    template_name = 'inventory/food_sets.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    
    def get_context_data(self, **kwargs):
        """Add the menu list to the context."""
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['menu_list'] = menu.objects.all()
        context['food_list'] = food.objects.all()
        return context


class NewFood(LoginRequiredMixin, View):
    """This view will allow the user to build a trip through a form."""
    
    form_class = FoodForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            newFood = form.save(commit=False) 

            food_name = form.cleaned_data['food_name']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            warehouse = form.cleaned_data['warehouse']

            newFood.save()

            if newFood is not None:
                return redirect('inventory:meals')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})


class MealUpdate(LoginRequiredMixin, UpdateView):
    """This view will allow the user to update meals."""

    model = meal
    form_class = MealForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get_success_url(self):
        """Will allow the user to return to the main food page."""
        return reverse_lazy('inventory:meals', kwargs={'pk': self.kwargs['pk']})


class MenuUpdate(LoginRequiredMixin, UpdateView):
    """This view will allow the user to update menus."""

    model = menu
    form_class = MenuForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get_success_url(self):
        """Will allow the user to return to the main food page."""
        return reverse_lazy('inventory:meals', kwargs={'pk': self.kwargs['pk']})

class MenuBuilder(LoginRequiredMixin, View):
    """This view will allow the user to build a trip through a form."""
    
    form_class = MenuForm
    template_name = 'inventory/new-menu.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    
    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            newMenu = form.save(commit=False) 

            menu_name = form.cleaned_data['menu_name']
            meal_name = form.cleaned_data['meal_name']

            newMenu.save()

            if newMenu is not None:
                return redirect('inventory:meals')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})


class MealBuilder(LoginRequiredMixin, View):
    """This view will allow the user to build a trip through a form."""
    
    form_class = MealForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    
    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            newMeal = form.save(commit=False) 

            meal_name = form.cleaned_data['meal_name']
            items = form.cleaned_data['items']
            description = form.cleaned_data['description']

            newMeal.save()

            if newMeal is not None:
                return redirect('inventory:meals')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})


class FoodDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """Will allow the user to delete food from the database."""
    model = food
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:meals')
    login_url = '/'
    redirect_field_name = 'redirect_to'


class SuppliesView(LoginRequiredMixin, generic.ListView):
    """Display a table of inventory for the user."""

    model = supplies
    template_name = 'inventory/supplies_list.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    
    def get_queryset(self):
        return supplies.objects.all()

    def get_context_data(self, **kwargs):
        # get the context data from the generic list view
        context = super().get_context_data(**kwargs)
        # add the filter to the context that will go to the template
        context['filter'] = SupplyFilter(self.request.GET, queryset=self.get_queryset())
        return context
    

class AddSupply(LoginRequiredMixin, View):
    # allow an item to be added to the table/database
    form_class = SupplyForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            supply = form.save(commit=False) # create an object so we can clean the data before saving it

            # now get the clean and normalize the data
            supplyName = form.cleaned_data['supplyName']
            category = form.cleaned_data['category']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            
            supply.save()

            if supply is not None:
                return redirect('inventory:supplies')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})


class FinancialListView(LoginRequiredMixin, generic.ListView):
    model = supplies
    template_name = "inventory/reports.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["supplies"] = supplies.objects.all()
        return context
    


class SupplyUpdate(LoginRequiredMixin, UpdateView):
    """This will allow the user to update an item."""
    model = supplies
    form_class = SupplyForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:supplies')


class SupplyDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """Will allow the user to delete a trip from the database."""
    model = supplies
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:supplies')
    login_url = '/'
    redirect_field_name = 'redirect_to'

      
class VansView(LoginRequiredMixin, generic.ListView):
    """Display a list of the vans for the user."""

    model = vans
    template_name = 'inventory/vans_list.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        """Return a list of all vans in the database."""
        return vans.objects.all()


class AddVan(LoginRequiredMixin, View):
    # allow an item to be added to the table/database
    form_class = VanForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            van = form.save(commit=False) # create an object so we can clean the data before saving it

            # now get the clean and normalize the data
            vanName = form.cleaned_data['vanName']
            condition = form.cleaned_data['condition']
            available = form.cleaned_data['available']
            mileage = form.cleaned_data['mileage']
            trailer = form.cleaned_data['trailer']
            comments = form.cleaned_data['comments']
            
            van.save()

            if van is not None:
                return redirect('inventory:vans')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})

class VanUpdate(LoginRequiredMixin, UpdateView):
    """This view will allow the user to update van information."""

    model = vans
    form_class = VanForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:vans')


class VanDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """Will allow the user to delete a trip from the database."""
    model = vans
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:vans')
    login_url = '/'
    redirect_field_name = 'redirect_to'


class UserFormView(LoginRequiredMixin, View):
    # what is the form's blueprint/class?
    form_class = UserForm
    template_name = 'inventory/registration_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    # whenever the user calls the form it's a get request, go here and display a blank form
    def get(self, request):
        form = self.form_class(None)# no data by default in the blank form
        return render(request, self.template_name, {'form': form})
    
    # process form data
    def post(self, request):
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            user = form.save(commit=False) # create an object from the form, but don't save the form's data to the database yet

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()# now save them to the database

            # returns User onjects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # request.user.username
                    # now redirect them to a page after login
                    return redirect('inventory:index')
                    
        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})    


class TripBuilder(LoginRequiredMixin, View):
    """This view will allow the user to build a trip through a form."""
    
    form_class = TripForm
    template_name = 'inventory/trip_builder.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    
    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            trip = form.save(commit=False) # create an object so we can clean the data before saving it

            # now get the clean and normalize the data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            comments = form.cleaned_data['comments']
            payment_status = form.cleaned_data['payment_status']
            trip_start = form.cleaned_data['trip_start']
            trip_end = form.cleaned_data['trip_end']
            van_used = form.cleaned_data['van_used']
            kayak_used = form.cleaned_data['kayak_used']
            menu = form.cleaned_data['menu']
            extra_meals_purchased = form.cleaned_data['extra_meals_purchased']
            #extra_food_purchased = form.cleaned_data['extra_food_purchased']
            extra_supplies = form.cleaned_data['extra_supplies']
            if (trip_end is None and trip_start is None):
                trip.save()
            elif (trip_end < trip_start):
                return render(request, self.template_name, {'form': form})
            

            trip.save()

            if trip is not None:
                return redirect('inventory:view-trips')
        
        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})

class TripManager(LoginRequiredMixin, generic.ListView):
    """This view will display the trips in the db in card fashion."""

    model = trips
    template_name = 'inventory/trip_manager.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return trips.objects.all().order_by('trip_start')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.date.today()
        return context



class TripDetails(LoginRequiredMixin, generic.DetailView):
    """This view will be used to display the details of a trip from the view trips page."""
    
    model = trips
    template_name = 'inventory/trip_details.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    #form_class = itineraryform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.date.today()
        return context
    

class TripUpdate(LoginRequiredMixin, UpdateView):
    """This view will allow the user to update trip information."""

    model = trips
    form_class = TripForm
    template_name = 'inventory/trip_builder.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get_success_url(self):
        """Will allow the user to return to the details page of that trip after updating."""
        return reverse_lazy('inventory:details', kwargs={'pk': self.kwargs['pk']})


class TripDelete(LoginRequiredMixin, DeleteView):
    """Will allow the user to delete a trip from the database."""
    model = trips
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:view-trips')
    login_url = '/'
    redirect_field_name = 'redirect_to'


class VanKitView(LoginRequiredMixin, generic.ListView):
    """Display list of VanKits for user"""

    model = van_kit
    template_name = 'inventory/vankit.html'
    login_url = '/'
    redirect_field_name = 'redirect_to' 

    def get_context_data(self, **kwargs):
        # call the super parent class and get the context data
        context = super().get_context_data(**kwargs)
        # now add in our specific query set
        context['master_list'] = VanKitMasterlist.objects.all()
        return context


class AddVanKit(LoginRequiredMixin, View):
    # allow an item to be added to the table/database
    form_class = VanKitForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            vankit = form.save(commit=False) # create an object so we can clean the data before saving it

            # now get the clean and normalize the data
            van_kit_name = form.cleaned_data['van_kit_name']
            vanName = form.cleaned_data['vanName']
            Available = form.cleaned_data['Available']
            comments = form.cleaned_data['comments']
            
            vankit.save()

            if vankit is not None:
                return redirect('inventory:vankit')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})


class VanKitUpdate(LoginRequiredMixin, UpdateView):
    """This view will allow the user to update vk information."""

    model = van_kit
    form_class = VanKitForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:vankit')


class VanKitDelete(LoginRequiredMixin, DeleteView):
    """Will allow the user to delete a vk from the database."""
    model = van_kit
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:vankit')
    login_url = '/'
    redirect_field_name = 'redirect_to'


class AddVKMasterlist(LoginRequiredMixin, View):
    # allow an item to be added to the table/database
    form_class = VKMasterlistForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            vkml = form.save(commit=False) # create an object so we can clean the data before saving it

            # now get the clean and normalize the data
            supplyName = form.cleaned_data['supplyName']
            supplyQuantity = form.cleaned_data['supplyQuantity']

            vkml.save()

            if vkml is not None:
                return redirect('inventory:vankit')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})


class VKMasterlistUpdate(LoginRequiredMixin, UpdateView):
    """This view lets user update vkmasterlist."""
    model = VanKitMasterlist
    form_class = VKMasterlistForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:vankit')


class VKMasterlistDelete(LoginRequiredMixin, DeleteView):
    """Will allow the user to delete a vkml from the database."""
    model = VanKitMasterlist
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:vankit')
    login_url = '/'
    redirect_field_name = 'redirect_to'