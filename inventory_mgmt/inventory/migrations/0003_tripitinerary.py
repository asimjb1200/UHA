# Generated by Django 2.1.7 on 2019-04-29 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_vankitmasterlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='tripItinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival', models.TimeField()),
                ('dropoff', models.TimeField()),
                ('activities', models.CharField(max_length=100)),
                ('trips', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.trips')),
            ],
        ),
    ]
