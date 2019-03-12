from django.contrib import admin
from .models import vans, van_kit, supplies, food, trips, KitSupplies, menu, meal, menu_meals, MealItem, kayak, warehouse, employee, customer, trailers
# Register your models here so they'll show in the admin page.
# only need admin classes for many to many relationships
class van_kitAdmin(admin.ModelAdmin):
    list_display = ('van_kit_name', 'vanName')# What columns do I want in the db
    search_fields = ['van_kit_name'] # able to search through van kits by the van kit number
    filter_horizontal = ('supply_name',)

class tripsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'payment_status')# display all trips in the db by the customer name
    search_fields = ['last_name', 'trip_start', 'payment_status'] # able to search through trips by customer name
    filter_horizontal = ('extra_food_purchased','extra_supplies','kayak_used','extra_meals_purchased', 'van_used')

class KitSuppliesAdmin(admin.ModelAdmin):
    list_display = ('supplyName', 'vanKit', 'quantity')
    search_fields = ['vanKit__van_kit_name']

class customerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ['first_name', 'last_name']

class trailersAdmin(admin.ModelAdmin):
    list_display = ('trailer_name', 'warehouse','condition')
    search_fields = ['trailer_name']

class kayakAdmin(admin.ModelAdmin):
    list_display = ('kayak_name', 'warehouse','condition')
    search_fields = ['kayak_name']

class menu_mealsAdmin(admin.ModelAdmin):
    list_display = ('meal_name', 'meal_qty', 'menu_name')
    search_fields = ['meal_name__meal_name', 'menu_name__menu_name']

class MealItemAdmin(admin.ModelAdmin):
    list_display = ('foodName', 'mealName', 'quantity')
    search_fields = ['mealName__meal_name', 'foodName__food_name']

admin.site.register(vans)
admin.site.register(KitSupplies, KitSuppliesAdmin)
admin.site.register(van_kit, van_kitAdmin)
admin.site.register(supplies)
admin.site.register(trips, tripsAdmin)
admin.site.register(food)
admin.site.register(customer, customerAdmin)
admin.site.register(trailers, trailersAdmin)
admin.site.register(employee)
admin.site.register(kayak, kayakAdmin)
admin.site.register(menu)
admin.site.register(meal)
admin.site.register(MealItem, MealItemAdmin)
admin.site.register(menu_meals, menu_mealsAdmin)
admin.site.register(warehouse)