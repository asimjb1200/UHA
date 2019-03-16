from django.views import generic
from django.shortcuts import render
from .models import supplies, van_kit, vans
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
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
    

class TripBuilder(View):
    """This view will allow the user to build a trip."""
    
    form_class = TripForm
    template_name = 'inventory/trip_builder.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})