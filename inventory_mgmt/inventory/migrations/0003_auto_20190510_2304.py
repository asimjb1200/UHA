# Generated by Django 2.1.7 on 2019-05-11 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20190510_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripitinerary',
            name='it_title',
            field=models.CharField(max_length=50),
        ),
    ]
