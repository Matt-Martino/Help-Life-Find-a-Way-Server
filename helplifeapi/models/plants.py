from django.db import models
from django.contrib.auth.models import User


class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available = models.BooleanField(default=False)
    new_plant_care = models.CharField(max_length=250)
    plant_age = models.CharField(max_length=50)
    plant_name = models.CharField(max_length=50)
    plant_image = models.CharField(max_length=50)
    

  