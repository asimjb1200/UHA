from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class customer(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    phone_number = PhoneNumberField(blank=False)
    email = models.EmailField(max_length=254, blank=False)
    group_size = models.PositiveSmallIntegerField(blank=False, default=0)

    def __str__(self):
        return self.first_name + " " + self.last_name


class employee(customer):

    role = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class warehouse(models.Model):
    location = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.location


class trailers(models.Model):
    class Meta:
        verbose_name_plural = "trailers"
    choices = (
        ('Ready', 'No Issues'),
        ('Work Needed', 'Issues identified'),
        ('Off-Limits', 'Not usable for treks')
    )
    trailer_name = models.CharField(max_length=50, unique=True)
    warehouse = models.ForeignKey(warehouse, on_delete=models.CASCADE)
    condition = models.CharField(max_length=50, choices=choices)
    available = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.trailer_name


class kayak(models.Model):
    choices = (
        ('Ready', 'No Issues'),
        ('Work Needed', 'Issues identified'),
        ('Off-Limits', 'Not usable for treks')
    )
    kayak_name = models.CharField(max_length=50)
    warehouse = models.ForeignKey(warehouse, on_delete=models.CASCADE)
    condition = models.CharField(max_length=50, choices=choices)
    available = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.kayak_name


class vans(models.Model):
    class Meta:
        verbose_name_plural = "vans"

    choices = (
        ('Ready', 'No Issues'),
        ('Work Needed', 'Issues identified'),
        ('Off-Limits', 'Not usable for treks')
    )

    vanName = models.CharField(max_length=30, unique=True, blank=False)
    condition = models.CharField(max_length=50, choices=choices)
    available = models.BooleanField(default=True, blank=False)
    mileage = models.PositiveIntegerField()
    trailer = models.ForeignKey(trailers, on_delete=models.CASCADE, blank=True, null=True)
    comments = models.TextField(blank=True, null=True, max_length=150)

    # set up how the vans will be referenced in the admin page
    def __str__(self):
        return self.vanName


class supplies(models.Model):
    class Meta:
        verbose_name_plural = "supplies"
    # limit the user to selecting a pre-set category
    choices = (
        ('CREW-GEAR', 'CREW-GEAR'),
        ('CONSUMABLE', 'CONSUMABLE'),
        ('BACK-COUNTRY', 'BACK-COUNTRY')
    )
    # if they go over the max length, we'll get a 500 error
    supplyName = models.CharField(max_length=30, blank=False)
    category = models.CharField(max_length=20, choices=choices, blank=False)
    quantity = models.PositiveSmallIntegerField(blank=False)  # set up default
    # inputting price is optional
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.supplyName

    def show_qty(self):
        return self.quantity

    def _get_total(self):
        return self.quantity * self.price

    total = property(_get_total)


class van_kit(models.Model):
    supply_name = models.ManyToManyField(supplies, through='KitSupplies', through_fields=('vanKit', 'supplyName'), related_name="supplies")
    van_kit_name = models.CharField(max_length=100)
    vanName = models.OneToOneField(vans, on_delete=models.CASCADE)
    Available = models.BooleanField(default=True, blank=False)
    comments = models.TextField(blank=True, null=True, max_length=150)

    def __str__(self):
        return self.van_kit_name


class VanKitMasterlist(models.Model):
    # over max length, return error
    supplyName = models.CharField(max_length=100, blank=False)
    supplyQuantity = models.PositiveSmallIntegerField(blank=False)  # set up default

    def __str__(self):
        return self.supplyName

    def show_qty(self):
        return self.supplyQuantity


class KitSupplies(models.Model):
    supplyName = models.ForeignKey(supplies, on_delete=models.CASCADE)
    vanKit = models.ForeignKey(van_kit, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(blank=False)

    def __str__(self):
        return str(self.supplyName)

    class Meta:
        verbose_name_plural = 'Kit Supplies'


class food(models.Model):
    class Meta:
        verbose_name_plural = "food"
    food_name = models.CharField(max_length=100, blank=False)
    # inputting price is optional
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(blank=False)
    warehouse = models.ManyToManyField(warehouse, related_name='warehouse', through='foodWarehouse', through_fields=('food_name', 'warehouse'))

    def __str__(self):
        return self.food_name

    def _get_total(self):
        return self.quantity * self.price

    total = property(_get_total)


class foodWarehouse(models.Model):
    food_name = models.ForeignKey(food, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(warehouse, on_delete=models.CASCADE)
    qty = models.PositiveSmallIntegerField(blank=False)


class meal(models.Model):
    meal_name = models.CharField(max_length=30, unique=True, blank=False)
    # , through="MealItem", through_fields=("mealName", "foodName")
    items = models.ManyToManyField(food)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.meal_name


# class MealItem(models.Model):
#     mealName = models.ForeignKey(meal, on_delete=models.CASCADE)
#     foodName = models.ForeignKey(food, on_delete=models.CASCADE)
#     quantity = models.PositiveSmallIntegerField()


class menu(models.Model):
    menu_name = models.CharField(max_length=50, unique=True)
    # , through="menu_meals", through_fields=("menu_name", "meal_name")
    meal_name = models.ManyToManyField(meal)

    def __str__(self):
        return self.menu_name


# class menu_meals(models.Model):
#     class Meta:
#         verbose_name_plural = "menu meals"
#     menu_name = models.ForeignKey(menu, on_delete=models.CASCADE)
#     meal_name = models.ForeignKey(meal, on_delete=models.CASCADE)
#     meal_qty = models.PositiveSmallIntegerField(null=True)


class trips(models.Model):
    class Meta:
        verbose_name_plural = "trips"

    choices = (
        ('Outreach', 'customer contacted'),
        ('Deposit Made', 'payment secured'),
        ('Trip Started', 'Trip ready')
    )

    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    comments = models.TextField(blank=True, null=True, max_length=300)
    payment_status = models.CharField(max_length=150, choices=choices, null=True)
    trip_start = models.DateField(blank=True, null=True)
    trip_end = models.DateField(blank=True, null=True)
    van_used = models.ForeignKey(vans, on_delete=models.CASCADE, blank=True)
    kayak_used = models.ManyToManyField(kayak, related_name="kayak", blank=True)
    menu = models.ForeignKey(menu, on_delete=models.CASCADE, related_name="trip_menu", null=True)
    extra_meals_purchased = models.ManyToManyField(meal, related_name="trip_meals", blank=True)
    extra_food_purchased = models.ManyToManyField(food, related_name='food_used', blank=True)
    extra_supplies = models.ManyToManyField(supplies, related_name='trip_extras', blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
