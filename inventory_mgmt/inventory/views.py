# Designed by Asim J.B. and Sean M. for use by Alaska Ultimate High Adventure employees.
# Circa 2019
from django.views import generic
from django.shortcuts import render, redirect
from .models import tripItinerary, supplies, van_kit, vans, trips, meal, menu, food, customer, warehouse, trailers, kayak, VanKitMasterlist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .filters import SupplyFilter, CustomerFilter, FoodFilter
from .forms import  itineraryform, SupplyForm, WarehouseForm, KayakForm, TrailerForm, FoodForm, CustomerForm, MenuForm, UserForm, TripForm, VanForm, MealForm, VanKitForm, VKMasterlistForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages

@login_required
def index(request):
    """Display the landing page of the website."""
    return render(request, 'inventory/index.html')


class itineraryDetails(LoginRequiredMixin, generic.DetailView):
    """This view will be used to display the details of a itinerary."""
    
    model = tripItinerary
    template_name = 'inventory/it-details.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'


class itineraryDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """Will allow the user to delete itineraries."""

    model = tripItinerary
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:viewitinerary')
    login_url = '/'
    redirect_field_name = 'redirect_to'


class itineraryView(LoginRequiredMixin, generic.ListView):
    """View all itineraries in the database."""
    
    model = tripItinerary
    template_name = 'inventory/view-itinerary.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        """Return a list of all itineraries."""
        return tripItinerary.objects.all()

    # def get_context_data(self, **kwargs):
    #     # get the context data from the generic list view
    #     context = super().get_context_data(**kwargs)
    #     # add the filter to the context that will go to the template
    #     context['filter'] = ItineraryFilter(self.request.GET, queryset=self.get_queryset())
    #     return context

# class ItineraryList(ListView):
#     model = tripItinerary
#     template_name = 'inventory/view-itinerary.html'
#     success_url = reverse_lazy('index')
#     fields = ['name']

class createItinerary(LoginRequiredMixin, View):
    """Create a new itinerary."""

    model = tripItinerary
    #fields = ['first_name']
    template_name = 'inventory/itinerary-form.html'
    form_class = itineraryform
    login_url ='/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in user data, clean it, and then post it to the database."""
        form = self.form_class(request.POST) # pass in the user's data to that was submitted in form 

        if form.is_valid():
            schedule = form.save(commit=False) 

            #trips = form.cleaned_data['trips']
            itinerary = form.cleaned_data['itinerary']
            Itinerary_title = form.cleaned_data['Itinerary_title']

            schedule.save()

            if schedule is not None:
                return redirect('inventory:viewitinerary')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})


class ItineraryUpdate(LoginRequiredMixin, UpdateView):
    """This view will allow the user to update itinerary information."""

    model = tripItinerary
    form_class = itineraryform
    template_name = 'inventory/itinerary-form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:viewitinerary')
    

    # def get_context_data(self, **kwargs):
    #     data = super(createItinerary, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         data['familymembers'] = ItineraryFormSet(self.request.POST)
    #     else:
    #         data['familymembers'] = ItineraryFormSet()
    #     return data
    
    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     familymembers = context['familymembers']
    #     with transaction.atomic():
    #         self.object = form.save()

    #         if familymembers.is_valid():
    #             familymembers.instance = self.object
    #             familymembers.save()

    #             #if familymembers is not None:
    #             #    return redirect('inventory:index')
                
    #     return super(createItinerary, self).form_valid(form)


    

# class ItineraryUpdate(LoginRequiredMixin, UpdateView):
#     model = tripItinerary
#     template_name = 'inventory/itinerary-form.html'
#     form_class = itineraryform
#     success_url = reverse_lazy('inventory:viewitinerary')
#     login_url = '/'
#     redirect_field_name = 'redirect_to'

    # def get_context_data(self, **kwargs):
    #     data = super(ItineraryUpdate, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         data['familymembers'] = ItineraryFormSet(self.request.POST, instance=self.object)
    #     else:
    #         data['familymembers'] = ItineraryFormSet(instance=self.object)
    #     return data
    
    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     familymembers = context['familymembers']
    #     with transaction.atomic():
    #         self.object = form.save()

    #         if familymembers.is_valid():
    #             familymembers.instance = self.object
    #             familymembers.save()

    #             #if familymembers is not None:
    #             #    return redirect('inventory:viewitinerary')
                
    #     return super(ItineraryUpdate, self).form_valid(form)


class Customers(LoginRequiredMixin, generic.ListView):
    """This page will display customer information."""

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
    """This page will display kayaks, trailers and warehouse locations."""

    model = warehouse
    template_name = 'inventory/warehouses.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

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
        form = self.form_class(
            request.POST)  # pass in the user's data to that was submitted in form

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
    """This view will allow the user to update trailer information."""

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
        form = self.form_class(
            request.POST)  # pass in the user's data to that was submitted in form

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
    """This view will allow the user to update kayaks."""

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
        form = self.form_class(
            request.POST)  # pass in the user's data to that was submitted in form

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
        form = self.form_class(
            request.POST)  # pass in the user's data to that was submitted in form

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
    """Display menus, meals and food to the user"""

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
        context['filter'] = FoodFilter(self.request.GET, queryset=food.objects.all())
        return context


class menuDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """Will allow the user to delete menus from the database."""

    model = menu
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:meals')
    login_url = '/'
    redirect_field_name = 'redirect_to'


class mealDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    """Will allow the user to delete meals from the database."""

    model = meal
    template_name = 'inventory/confirm_delete.html'
    success_url = reverse_lazy('inventory:meals')
    login_url = '/'
    redirect_field_name = 'redirect_to'


class NewFood(LoginRequiredMixin, View):
    """This view will allow the user to create new food."""

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
        form = self.form_class(request.POST)  # pass in the user's data to that was submitted in form

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

class FoodUpdate(LoginRequiredMixin, UpdateView):
    """This view will allow the user to update food."""

    model = food
    form_class = FoodForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:meals')


class MealUpdate(LoginRequiredMixin, UpdateView):
    """This view will allow the user to update meals."""

    model = meal
    form_class = MealForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:meals')


class MenuUpdate(LoginRequiredMixin, UpdateView):
    """This view will allow the user to update menus."""

    model = menu
    form_class = MenuForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    success_url = reverse_lazy('inventory:meals')

class MenuDetails(LoginRequiredMixin, generic.DetailView):
    """This view will be used to display the details of a menu."""
    
    model = menu
    template_name = 'inventory/menu_details.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'


class MealDetails(LoginRequiredMixin, generic.DetailView):
    """This view will be used to display the details of a meal."""
    
    model = meal
    template_name = 'inventory/meal_details.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    #form_class = itineraryform


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
        form = self.form_class(
            request.POST)  # pass in the user's data to that was submitted in form

        if form.is_valid():
            newMenu = form.save(commit=False)

            menu_name = form.cleaned_data['menu_name']
            meal_name = form.cleaned_data['meal_name']

            newMenu.save()
            form.save_m2m()

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
        form = self.form_class(
            request.POST)  # pass in the user's data to that was submitted in form

        if form.is_valid():
            newMeal = form.save(commit=False)

            meal_name = form.cleaned_data['meal_name']
            items = form.cleaned_data['items']
            description = form.cleaned_data['description']

            newMeal.save()
            form.save_m2m()

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
    """Add a supply to the database."""

    form_class = SupplyForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in data, clean it, and then post it to the database."""
        form = self.form_class(
            request.POST)  # pass in the user's data to that was submitted in form

        if form.is_valid():
            # create an object so we can clean the data before saving it
            supply = form.save(commit=False)

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
    """Reports on inventory prices."""

    model = supplies
    template_name = "inventory/reports.html"


    def get_context_data(self, **kwargs):
        """Getting total prices to be displayed in the reports page."""

        supplyTotal = 0
        foodTotal = 0
        cgTotal = 0
        bcTotal = 0
        conTotal = 0
        grandTotal = 0

        for cg in supplies.objects.all():
            if cg.category == "CREW-GEAR":
                cgTotal += int(cg.total)

        for bc in supplies.objects.all():
            if bc.category == "BACK-COUNTRY":
                bcTotal += int(bc.total)

        for consumable in supplies.objects.all():
            if consumable.category == "CONSUMABLE":
                conTotal += int(consumable.total)
        
        for supply in supplies.objects.all():
            supplyTotal += int(supply.total)
        
        for item in food.objects.all():
            foodTotal += int(item.total)

        context = super().get_context_data(**kwargs)
        context["supplies"] = supplies.objects.all()
        context["supplyTotal"] = supplyTotal
        context["food"] = food.objects.all()
        context["foodTotal"] = foodTotal
        context["cgTotal"] = cgTotal
        context["bcTotal"] = bcTotal
        context["conTotal"] = conTotal
        context["grandTotal"] = foodTotal + supplyTotal

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
    """Adding a van to the database."""

    form_class = VanForm
    template_name = 'inventory/new_supply.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        """Return a blank form to the user to be filled out."""
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Take in data, clean it, and then post it to the database."""
        form = self.form_class(
            request.POST)  # pass in the user's data to that was submitted in form

        if form.is_valid():
            # create an object so we can clean the data before saving it
            van = form.save(commit=False)

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
    """Creating a new user."""

    form_class = UserForm
    template_name = 'inventory/registration_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    # whenever the user calls the form it's a get request, go here and display a blank form
    def get(self, request):
        form = self.form_class(None)  # no data by default in the blank form
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        # pass in the user's data to that was submitted in form
        form = self.form_class(request.POST)

        if form.is_valid():
            # create an object from the form, but don't save the form's data to the database yet
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()  # now save them to the database

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
        form = self.form_class(request.POST)  # pass in the user's that was submitted in form

        def toggleVan(self, car):
            van1 = vans.objects.filter(vanName=car.vanName)
            van1.update(available=False)

        def toggleKayak(self, kayak_used):
            for choice in kayak_used:
                current = kayak.objects.get(kayak_name=choice.kayak_name)
                current.available = False
                current.save()

        if form.is_valid():
            # create an object so we can clean the data before saving it
            trip = form.save(commit=False)
            today = datetime.date.today()

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
            extra_supplies = form.cleaned_data['extra_supplies']
            trip_Itinerary = form.cleaned_data['trip_Itinerary']     

            if (trip_end < trip_start):
                return render(request, self.template_name, {'form': form})

            if van_used is not None:
                # Checking the entire trip database for vans that have already been booked
                if trips.objects.filter(van_used = form.cleaned_data['van_used']).exists():
                    for next in trips.objects.filter(van_used=van_used):
                            
                            if trip_start >= next.trip_start and trip_end <= next.trip_end:
                                if van_used == next.van_used:
                                    messages.warning(request, van_used.vanName + ' is in use during that time period. Pick another vehicle or change trip dates.')
                                    return render(request, self.template_name, {'form': form})
                            
                            elif trip_start <= next.trip_end and trip_start >= next.trip_start:
                                if van_used == next.van_used:
                                    messages.warning(request, van_used.vanName + ' is in use during that time period. Pick another vehicle or change trip dates.')
                                    return render(request, self.template_name, {'form': form})
                            
                            elif trip_end >= next.trip_start and trip_end <= next.trip_end:
                                if van_used == next.van_used:
                                    messages.warning(request, van_used.vanName + ' is in use during that time period. Pick another vehicle or change trip dates.')
                                    return render(request, self.template_name, {'form': form})

                            elif next.trip_start >= trip_start and next.trip_end <= trip_end:
                                if van_used == next.van_used:
                                    messages.warning(request, van_used.vanName + ' is in use during that time period. Pick another vehicle or change trip dates.')
                                    return render(request, self.template_name, {'form': form})
                            
                            elif next.trip_start <= trip_end and next.trip_start >= trip_start:
                                if van_used == next.van_used:
                                    messages.warning(request, van_used.vanName + ' is in use during that time period. Pick another vehicle or change trip dates.')
                                    return render(request, self.template_name, {'form': form})
                            
                            elif next.trip_end >= trip_start and next.trip_end <= trip_end:
                                if van_used == next.van_used:
                                    messages.warning(request, van_used.vanName + ' is in use during that time period. Pick another vehicle or change trip dates.')
                                    return render(request, self.template_name, {'form': form})
                #toggleVan(self, van_used)
            
            if kayak_used is not None:
                toggleKayak(self, kayak_used)

            if (trip_end is None and trip_start is None):
                trip.save()
                form.save_m2m()

            trip.save()
            form.save_m2m()

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
        """Run checks on all trip objects to make sure dates don't hog availability."""
        for trip in trips.objects.all():
            trip.beg_check()
            trip.end_check()
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
    """Display list of VanKits for user."""

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
    """Add van kit to the database."""
   
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
        form = self.form_class(
            request.POST)  # pass in the user's data to that was submitted in form

        if form.is_valid():
            # create an object so we can clean the data before saving it
            vankit = form.save(commit=False)

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
    """Add item to the vankit master list."""

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
        form = self.form_class(
            request.POST)  # pass in the user's data to that was submitted in form

        if form.is_valid():
            # create an object so we can clean the data before saving it
            vkml = form.save(commit=False)

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
