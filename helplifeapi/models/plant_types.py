from django.db import models

class PlantType(models.Model):
    plant_type = models.CharField(max_length=50)
    

    