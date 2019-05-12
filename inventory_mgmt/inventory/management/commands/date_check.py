from django.core.management.base import BaseCommand, CommandError
from inventory.models import trips, vans
import datetime


class Command(BaseCommand):
    help ='update van availability by date'

    def add_arguments(self, parser):
        parser.add_argument('trips_id', nargs='+', type=int)

    def handle(self, *args, **options):
         """Will be used as a background task to make sure trips that have ended don't hog van availability."""
         today = datetime.date.today()
         trip = trips.objects.get(pk = options['trips_id'])
         name = trip.van_used

         if today > trip.trip_start and today > trip.trip_end:
            car = vans.objects.get(vanName = name)
            car.available = True
            car.save()

            
            