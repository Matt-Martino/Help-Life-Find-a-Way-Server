from django.db import models

class UserPlantPlantType(models.Model):
    plant_type = models.ForeignKey("PlantType", on_delete=models.CASCADE)
    plant = models.ForeignKey("Plant", on_delete=models.CASCADE)

   