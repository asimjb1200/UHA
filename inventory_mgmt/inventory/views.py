from django.views import generic
from django.shortcuts import render, redirect
from .models import supplies, van_kit, vans, trips
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .filters import SupplyFilter # import the filter
from .forms import TripForm, UserForm
import datetime

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



class TripManager(generic.ListView):
    """This view will display the trips in the db in card fashion."""

    model = trips
    template_name = 'inventory/trip_manager.html'

    def get_queryset(self):
        return trips.objects.all().order_by('trip_start')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.date.today()
        return context


class TripDetails(generic.DetailView):
    """This view will be used to display the details of a trip from the view trips page."""
    
    model = trips
    template_name = 'inventory/trip_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.date.today()
        return context
        
        
class VansView(generic.ListView):
    """Display a list of the vans for the user."""

    model = vans
    template_name = 'inventory/vans_list.html'

    def get_queryset(self):
        """Return a list of all vans in the database."""
        return vans.objects.all()
    

class UserFormView(View):
    # what is the form's blueprint/class?
    form_class = UserForm
    template_name = 'inventory/registration_form.html'

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

class TripUpdate(UpdateView):
    model = trips
    form_class = TripForm
    template_name = 'inventory/trip_builder.html'

    def get_success_url(self):
        return reverse_lazy('inventory:details', kwargs={'pk': self.kwargs['pk']})

class TripDelete(DeleteView):
    model = trips
    success_url = reverse_lazy('inventory:index')