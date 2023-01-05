from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class HelpLifeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_image_url = models.TextField()
    
    
    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def username(self):
        return f'{self.user.username}'

    @property
    def tokenNumber(self):
        token = Token.objects.get(user_id=self.user.id)
        return f'{token}'

    @property
    def email(self):
        return f'{self.user.email}'

    @property
    def total_plant_count(self):
        return self.__total_plant_count

    @total_plant_count.setter
    def total_plant_count(self, value):
        self.__total_plant_count = value

    @property
    def available_plant_count(self):
        return self.__available_plant_count

    @available_plant_count.setter
    def available_plant_count(self, value):
        self.__available_plant_count = value