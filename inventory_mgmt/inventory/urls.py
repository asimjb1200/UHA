from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'inventory'
urlpatterns = [
    url(r'^$', LoginView.as_view(), name="login"),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^home/$', views.index, name='index'),
    
    url(r'^reports/$', views.FinancialListView.as_view(), name="reports"),

    url(r'^other/$', views.OtherCompanyInfo.as_view(), name="other"),
    url(r'^other/add-warehouse/$', views.NewWarehouse.as_view(), name='add-warehouse'),
    url(r'^other/add-trailer/$', views.NewTrailer.as_view(), name='add-trailer'),
    url(r'^other/edit-trailer/(?P<pk>[0-9]+)/$', views.TrailerUpdate.as_view(), name='edit-trailer'),
    url(r'^other/add-kayak/$', views.NewKayak.as_view(), name='add-kayak'),
    url(r'^other/edit-kayak/(?P<pk>[0-9]+)/$', views.KayakUpdate.as_view(), name='edit-kayak'),

    url(r'^customers/$', views.Customers.as_view(), name="customers"),
    url(r'^customers/add/$', views.NewCustomer.as_view(), name='add-customer'),
    url(r'^customers/edit/(?P<pk>[0-9]+)/$', views.CustomerUpdate.as_view(), name='edit-customer'),

    url(r'^food/$', views.MealsView.as_view(), name='meals'),
    url(r'^food/build_meal/$', views.MealBuilder.as_view(), name='meal-builder'),
    url(r'^food/build_menu/$', views.MenuBuilder.as_view(), name='menu-builder'),
    url(r'^food/edit-meal/(?P<pk>[0-9]+)/$', views.MealUpdate.as_view(), name='edit-meal'),
    url(r'^food/edit-menu/(?P<pk>[0-9]+)/$', views.MenuUpdate.as_view(), name='edit-menu'),
    url(r'^food/add/$', views.NewFood.as_view(), name='add-food'),
    url(r'^food/(?P<pk>[0-9]+)/delete/$', views.FoodDelete.as_view(), name='delete-food'),

    url(r'^supplies/$', views.SuppliesView.as_view(), name='supplies'),
    url(r'^supplies/add/$', views.AddSupply.as_view(), name='add-supply'),
    url(r'^supplies/edit/(?P<pk>[0-9]+)/$', views.SupplyUpdate.as_view(), name='edit-supply'),
    url(r'^supplies/(?P<pk>[0-9]+)/delete/$', views.SupplyDelete.as_view(), name='delete-supply'),

    url(r'^vans/$', views.VansView.as_view(), name='vans'),
    url(r'^vans/add/$', views.AddVan.as_view(), name='add-van'),
    url(r'^vans/(?P<pk>[0-9]+)/delete/$', views.VanDelete.as_view(), name='delete-van'),
    url(r'^vans/edit/(?P<pk>[0-9]+)/$', views.VanUpdate.as_view(), name='edit-van'),

    url(r'^trips/view-trips/$', views.TripManager.as_view(), name='view-trips'),
    url(r'^trips/build_trip/$', views.TripBuilder.as_view(), name='trip-builder'),
    url(r'^trips/view-trips/trip_details/(?P<pk>[0-9]+)/$', views.TripDetails.as_view(), name='details'),
    url(r'^trips/view-trips/trip_details/update/(?P<pk>[0-9]+)/$', views.TripUpdate.as_view(), name='update-trip'),
    url(r'^trips/view-trips/(?P<pk>[0-9]+)/delete/$', views.TripDelete.as_view(), name='delete-trip'),
    
    url(r'^vankits/$', views.VanKitView.as_view(), name='vankit'),
    url(r'^vankits/add/$', views.AddVanKit.as_view(), name='add-vankit'),
    url(r'^vankits/(?P<pk>[0-9]+)/delete/$', views.VanKitDelete.as_view(), name='delete-vankits'),
    url(r'^vankits/edit-vk/(?P<pk>[0-9]+)/$', views.VanKitUpdate.as_view(), name='edit-vankits'),
    url(r'^vankits/add-vkml/$', views.AddVKMasterlist.as_view(), name='add-vkml'),
    url(r'^vankits/edit-vkml/(?P<pk>[0-9]+)/$', views.VKMasterlistUpdate.as_view(), name='edit-vkml'),
    url(r'^vankits/delete-vkml/(?P<pk>[0-9]+)/$', views.VKMasterlistDelete.as_view(), name='delete-vkml'),


    url(r'^triplist/$', views.TripList.as_view(), name='triplist'),
    url(r'^trips/view-trips/trip_details/update-itinerary/$', views.createItinerary.as_view(), name='createitinerary'),


]
