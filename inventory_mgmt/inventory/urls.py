from django.conf.urls import url
from . import views

app_name = 'inventory'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^supplies/$', views.SuppliesView.as_view(), name='supplies'),
    url(r'^vans/$', views.VansView.as_view(), name='vans'),
    url(r'^trips/build_trip/$', views.TripBuilder.as_view(), name='trip-builder'),
]
