from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView

app_name = 'inventory'
urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^$', views.index, name='index'),
    url(r'^supplies/$', views.SuppliesView.as_view(), name='supplies'),
    url(r'^vans/$', views.VansView.as_view(), name='vans'),
    url(r'^trips/$', views.VansView.as_view(), name='trips'),
    url(r'^trips/view-trips/$', views.TripManager.as_view(), name='view-trips'),
    url(r'^trips/build_trip/$', views.TripBuilder.as_view(), name='trip-builder'),
    url(r'^trips/view-trips/trip_details/(?P<pk>[0-9]+)/$', views.TripDetails.as_view(), name='details'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
]
