from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'inventory'
urlpatterns = [
    url(r'^$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^home/$', views.index, name='index'),
    url(r'^supplies/$', views.SuppliesView.as_view(), name='supplies'),
    url(r'^vans/$', views.VansView.as_view(), name='vans'),
    url(r'^trips/view-trips/$', views.TripManager.as_view(), name='view-trips'),
    url(r'^trips/build_trip/$', views.TripBuilder.as_view(), name='trip-builder'),
    url(r'^trips/view-trips/trip_details/(?P<pk>[0-9]+)/$', views.TripDetails.as_view(), name='details'),
    url(r'^trips/view-trips/trip_details/update/(?P<pk>[0-9]+)/$', views.TripUpdate.as_view(), name='update-trip'),
    url(r'^trips/view-trips/(?P<pk>[0-9]+)/delete/$', views.TripDelete.as_view(), name='delete-trip'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
]
