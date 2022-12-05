from django.db import models

class CareTip(models.Model):
    plant_tip_label = models.CharField(max_length=50)
    description_of_tip = models.CharField(max_length=250)

