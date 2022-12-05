from django.db import models

class PlantCareTip(models.Model):
    care_tip = models.ForeignKey("CareTip", on_delete=models.CASCADE)
    plant = models.ForeignKey("Plant", on_delete=models.CASCADE)

    