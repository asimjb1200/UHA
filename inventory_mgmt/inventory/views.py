from django.views import generic
from django.shortcuts import render
from .models import supplies, van_kit, vans
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.views.generic import View

# Create your views here.
def index(request):
    """Display the landing page of the website."""
    return render(request, 'inventory/index.html')

class SuppliesView(generic.ListView):
    """Display a table of inventory for the user."""

    model = supplies
    template_name = 'inventory/supplies_list.html'

    def get_queryset(self):
        """Return a list of all the supplies in an object."""
        return supplies.objects.all()