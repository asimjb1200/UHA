# Generated by Django 2.1.7 on 2019-04-08 17:41

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('group_size', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=100)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('quantity', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name_plural': 'food',
            },
        ),
        migrations.CreateModel(
            name='foodWarehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveSmallIntegerField()),
                ('food_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.food')),
            ],
        ),
        migrations.CreateModel(
            name='kayak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kayak_name', models.CharField(max_length=50)),
                ('condition', models.CharField(choices=[('Ready', 'No Issues'), ('Work Needed', 'Issues identified'), ('Off-Limits', 'Not usable for treks')], max_length=50)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='KitSupplies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name_plural': 'Kit Supplies',
            },
        ),
        migrations.CreateModel(
            name='meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MealItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('foodName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.food')),
                ('mealName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.meal')),
            ],
        ),
        migrations.CreateModel(
            name='menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='menu_meals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_qty', models.PositiveSmallIntegerField()),
                ('meal_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.meal')),
                ('menu_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.menu')),
            ],
            options={
                'verbose_name_plural': 'menu meals',
            },
        ),
        migrations.CreateModel(
            name='supplies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplyName', models.CharField(max_length=30)),
                ('category', models.CharField(choices=[('CREW-GEAR', 'CREW-GEAR'), ('CONSUMABLE', 'CONSUMABLE'), ('BACK-COUNTRY', 'BACK-COUNTRY')], max_length=20)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'verbose_name_plural': 'supplies',
            },
        ),
        migrations.CreateModel(
            name='trailers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trailer_name', models.CharField(max_length=50, unique=True)),
                ('condition', models.CharField(choices=[('Ready', 'No Issues'), ('Work Needed', 'Issues identified'), ('Off-Limits', 'Not usable for treks')], max_length=50)),
                ('available', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'trailers',
            },
        ),
        migrations.CreateModel(
            name='trips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('comments', models.TextField(blank=True, null=True)),
                ('payment_status', models.CharField(choices=[('Outreach', 'customer contacted'), ('Deposit Made', 'payment secured'), ('Trip Started', 'Trip ready')], max_length=150, null=True)),
                ('trip_start', models.DateField(blank=True)),
                ('trip_end', models.DateField(blank=True)),
                ('extra_food_purchased', models.ManyToManyField(blank=True, related_name='food_used', to='inventory.food')),
                ('extra_meals_purchased', models.ManyToManyField(blank=True, related_name='trip_meals', to='inventory.meal')),
                ('extra_supplies', models.ManyToManyField(blank=True, related_name='trip_extras', to='inventory.supplies')),
                ('kayak_used', models.ManyToManyField(blank=True, related_name='kayak', to='inventory.kayak')),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trip_menu', to='inventory.menu')),
            ],
            options={
                'verbose_name_plural': 'trips',
            },
        ),
        migrations.CreateModel(
            name='van_kit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('van_kit_name', models.CharField(max_length=100)),
                ('Available', models.BooleanField(default=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('supply_name', models.ManyToManyField(related_name='supplies', through='inventory.KitSupplies', to='inventory.supplies')),
            ],
        ),
        migrations.CreateModel(
            name='vans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vanName', models.CharField(max_length=30, unique=True)),
                ('condition', models.CharField(choices=[('Ready', 'No Issues'), ('Work Needed', 'Issues identified'), ('Off-Limits', 'Not usable for treks')], max_length=50)),
                ('available', models.BooleanField(default=True)),
                ('mileage', models.PositiveIntegerField()),
                ('comments', models.TextField(blank=True, null=True)),
                ('trailer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.trailers')),
            ],
            options={
                'verbose_name_plural': 'vans',
            },
        ),
        migrations.CreateModel(
            name='warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='employee',
            fields=[
                ('customer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='inventory.customer')),
                ('role', models.CharField(max_length=100)),
            ],
            bases=('inventory.customer',),
        ),
        migrations.AddField(
            model_name='van_kit',
            name='vanName',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory.vans'),
        ),
        migrations.AddField(
            model_name='trips',
            name='van_used',
            field=models.ManyToManyField(blank=True, to='inventory.vans'),
        ),
        migrations.AddField(
            model_name='trailers',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse'),
        ),
        migrations.AddField(
            model_name='menu',
            name='meal_name',
            field=models.ManyToManyField(related_name='meals', through='inventory.menu_meals', to='inventory.meal'),
        ),
        migrations.AddField(
            model_name='meal',
            name='items',
            field=models.ManyToManyField(related_name='meal_items', through='inventory.MealItem', to='inventory.food'),
        ),
        migrations.AddField(
            model_name='kitsupplies',
            name='supplyName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.supplies'),
        ),
        migrations.AddField(
            model_name='kitsupplies',
            name='vanKit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.van_kit'),
        ),
        migrations.AddField(
            model_name='kayak',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse'),
        ),
        migrations.AddField(
            model_name='foodwarehouse',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse'),
        ),
        migrations.AddField(
            model_name='food',
            name='warehouse',
            field=models.ManyToManyField(related_name='warehouse', through='inventory.foodWarehouse', to='inventory.warehouse'),
        ),
    ]
