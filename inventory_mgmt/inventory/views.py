from django.views import generic
from django.shortcuts import render
from .models import supplies, van_kit, vans
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.views.generic import View


# Create your views here.
def index(request):
    return render(request, 'inventory/index.html')

class SuppliesView(generic.ListView):
    model = supplies
    template_name = 'inventory/supplies_list.html'
    context_object_name = "object_list"

    def get_queryset(self):
        return supplies.objects.all()