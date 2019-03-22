from django.views import generic
from django.shortcuts import render, redirect
from .models import supplies, van_kit, vans
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy
from django.views.generic import View
from .filters import SupplyFilter # import the filter
from .forms import TripForm

# Create your views here.
def index(request):
    """Display the landing page of the website."""
    return render(request, 'inventory/index.html')

class SuppliesView(generic.ListView):
    """Display a table of inventory for the user."""

    model = supplies
    template_name = 'inventory/supplies_list.html'
    
    def get_queryset(self):
        return supplies.objects.all()

    def get_context_data(self, **kwargs):
        # get the context data from the generic list view
        context = super().get_context_data(**kwargs)
        # add the filter to the context that will go to the template
        context['filter'] = SupplyFilter(self.request.GET, queryset=self.get_queryset())
        return context

    
    
class VansView(generic.ListView):
    """Display a list of the vans for the user."""

    model = vans
    template_name = 'inventory/vans_list.html'

    def get_queryset(self):
        """Return a list of all vans in the database."""
        return vans.objects.all()

class VanKitView(generic.ListView):
    """Display list of VanKits for user"""

    model = van_kit
    template_name = 'inventory/vankits.html'

    def get_queryset(self):
        """Return a list of all vankits in db"""
        return van_kit.objects.all()


class TripBuilder(View):
    """This view will allow the user to build a trip through a form."""
    
    form_class = TripForm
    template_name = 'inventory/trip_builder.html'

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
            extra_food_purchased = form.cleaned_data['extra_food_purchased']
            extra_supplies = form.cleaned_data['extra_supplies']

            trip.save()

            if trip is not None:
                return redirect('inventory:index')

        # if it doesn't work, have them try again
        return render(request, self.template_name, {'form': form})