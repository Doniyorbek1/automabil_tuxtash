from django.contrib import admin

# Register your models here.
from test_api.models import Parking, Place, Car

admin.site.register(Parking)
admin.site.register(Car)
admin.site.register(Place)
