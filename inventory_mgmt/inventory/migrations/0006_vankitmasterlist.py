# Generated by Django 2.1.7 on 2019-04-12 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20190407_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='VanKitMasterlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplyName', models.CharField(max_length=100)),
                ('supplyQuantity', models.PositiveSmallIntegerField()),
            ],
        ),
    ]