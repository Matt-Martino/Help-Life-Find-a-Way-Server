from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helplifeapi.models import Plant, HelpLifeUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PlantView(ViewSet):
    """plant view"""

    def retrieve(self, request, pk):
        try: 
            plant = Plant.objects.get(pk=pk)
        except Plant.DoesNotExist:
            return Response({"message": "Plant does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = PlantSerializer(plant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        filtered_plants = Plant.objects.all()
        
        if "user" in request.query_params:
            query_value = request.query_params["user"]
            token = Token.objects.get(key=query_value)
            user_id = token.user_id
            filtered_plants = filtered_plants.filter(user=user_id)

        serializer = PlantSerializer(filtered_plants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        help_life_user = HelpLifeUser.objects.get(user=request.auth.user)

        plant = Plant.objects.create(
            user = help_life_user,
            available = request.data["available"],
            new_plant_care = request.data["new_plant_care"],
            plant_age = request.data["plant_age"],
            plant_name = request.data["plant_name"],
            plant_image = request.data["plant_image"]
            )
        serializer = PlantSerializer(plant)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        plant = Plant.objects.get(pk=pk)
        plant.available = request.data["available"]
        plant.new_plant_care = request.data["new_plant_care"]
        plant.plant_age = request.data["plant_age"]
        plant.plant_name = request.data["plant_name"]
        plant.plant_image = request.data["plant_image"]
        plant.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        plant = Plant.objects.get(pk=pk)
        plant.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpLifeUser
        fields = ("username", )


class PlantSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)

    class Meta:
        model = Plant
        fields = ('id', 
                'user', 
                'available', 
                'new_plant_care', 
                'plant_age', 
                'plant_name', 
                'plant_image', )

