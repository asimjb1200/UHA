from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionModelAdmin
from .models import vans, van_kit, supplies, food, trips, menu, meal, kayak, warehouse, employee, customer, trailers, VanKitMasterlist
# Register your models here so they'll show in the admin page.

@admin.register(food)
class foodAdmin(ExportActionModelAdmin):
    list_display = ('food_name', 'price', 'quantity', 'warehouse')
    search_fileds =['food_name', 'warehouse']

@admin.register(vans)
class vansAdmin(ExportActionModelAdmin):
    list_display = ('vanName', 'mileage', 'condition', 'trailer')

@admin.register(van_kit)
class van_kitAdmin(ExportActionModelAdmin):
    """Configure how I want the database to look in the admin page."""

    list_display = ('van_kit_name', 'vanName')# What columns do I want in the db
    search_fields = ['van_kit_name'] # able to search through van kits by specific fields
    filter_horizontal = ('supply_name',)

@admin.register(trips)
class tripsAdmin(ExportActionModelAdmin):
    """Configure how I want the database to look in the admin page. Also making it searchable."""

    list_display = ('first_name', 'last_name', 'trip_start', 'trip_end', 'van_used')# display all trips in the db by the customer name
    search_fields = ['last_name', 'trip_start', 'payment_status'] # able to search through trips by customer name
    filter_horizontal = ('extra_supplies','kayak_used','extra_meals_purchased')

# @admin.register(KitSupplies)
# class KitSuppliesAdmin(ImportExportModelAdmin):
#     """Configure how I want the database to look in the admin page. Also making it searchable."""

#     list_display = ('supplyName', 'vanKit', 'quantity')
#     search_fields = ['vanKit__van_kit_name']

@admin.register(customer)
class customerAdmin(ExportActionModelAdmin):
    """Configure how I want the database to look in the admin page. Also making it searchable."""

    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ['first_name', 'last_name']

@admin.register(trailers)
class trailersAdmin(ExportActionModelAdmin):
    """Configure how I want the database to look in the admin page. Also making it searchable."""

    list_display = ('trailer_name', 'warehouse','condition')
    search_fields = ['trailer_name']

@admin.register(kayak)
class kayakAdmin(ExportActionModelAdmin):
    """Configure how I want the database to look in the admin page. Also making it searchable."""

    list_display = ('kayak_name', 'warehouse','condition')
    search_fields = ['kayak_name']

# class menu_mealsAdmin(ImportExportModelAdmin):
#     """Configure how I want the database to look in the admin page. Also making it searchable."""

#     list_display = ('meal_name', 'meal_qty', 'menu_name')
#     search_fields = ['meal_name__meal_name', 'menu_name__menu_name']

# class MealItemAdmin(ImportExportModelAdmin):
#     """Configure how I want the database to look in the admin page. Also making it searchable."""

#     list_display = ('foodName', 'mealName', 'quantity')
#     search_fields = ['mealName__meal_name', 'foodName__food_name']

@admin.register(supplies)
class suppliesAdmin(ExportActionModelAdmin):
    """Configure how I want the database to look in the admin page. Also making it searchable."""

    list_display = ('supplyName', 'category', 'quantity', 'price')
    search_fields = ['supplyName', 'category']

# class foodWarehouseAdmin(ImportExportModelAdmin):
#     """Configure how I want the database to look in the admin page. Also making it searchable."""

#     list_display = ('food_name', 'warehouse', 'qty')
#     search_fields = ['food_name__food_name', 'warehouse__warehouse']

@admin.register(warehouse)
class warehouseAdmin(ExportActionModelAdmin):
    list_display = ('id', 'location')

@admin.register(VanKitMasterlist)
class vankitmasterlistAdmin(ExportActionModelAdmin):
    pass


# admin.site.register(vans)
# admin.site.register(KitSupplies, KitSuppliesAdmin)
# #admin.site.register(van_kit, van_kitAdmin)
# admin.site.register(VanKitMasterlist)
# admin.site.register(supplies, suppliesAdmin)
# admin.site.register(trips, tripsAdmin)
# #admin.site.register(food)
# admin.site.register(customer, customerAdmin)
# admin.site.register(trailers, trailersAdmin)
# admin.site.register(employee)
# admin.site.register(kayak, kayakAdmin)
# admin.site.register(menu)
# admin.site.register(meal)
# # admin.site.register(MealItem, MealItemAdmin)
# # admin.site.register(menu_meals, menu_mealsAdmin)
# admin.site.register(warehouse, warehouseAdmin)
# #admin.site.register(foodWarehouse, foodWarehouseAdmin)