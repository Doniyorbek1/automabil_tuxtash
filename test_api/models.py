from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#cars model 

    

# place model
class Place(models.Model):
    place_name = models.CharField(max_length=200, blank=False)
    location = models.URLField(blank=False)
    parking_size = models.IntegerField(blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    
    def __str__(self) -> str:
        return self.place_name
    
class Car(models.Model):
    in_out_choice = (
        ('input', 'input'),
        ('output', 'output'),
    )
    parkin_name = models.ForeignKey(Place, on_delete=models.CASCADE)
    car_number = models.CharField(max_length=20, blank=False)
    in_out = models.CharField(max_length=20, choices=in_out_choice)
    count = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.car_number
# parking
class Parking(models.Model):
    all_place = models.ForeignKey(Place, on_delete=models.CASCADE)
    parking_time = models.DateTimeField(auto_now_add=True)
    parking_out_time = models.DateTimeField(blank=False)
    in_out_cars = models.IntegerField(default=0)
    free_place = models.IntegerField(default=0)
    car_number = models.ForeignKey(Car, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.all_place}, {self.free_place}'