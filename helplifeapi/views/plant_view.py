from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helplifeapi.models import Plant, HelpLifeUser, CareTip, PlantType
from django.contrib.auth.models import User

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
        
        if "myPlants" in request.query_params:
            help_user = HelpLifeUser.objects.get(user=request.auth.user)
            filtered_plants = Plant.objects.filter(user=help_user)

        if "user" in request.query_params:
            query_value = request.query_params["user"]
            help_user = HelpLifeUser.objects.get(user=query_value)
            filtered_plants = Plant.objects.filter(user=help_user)
        serializer = PlantSerializer(filtered_plants, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)

       

    def create(self, request):

        helpLifeUser = HelpLifeUser.objects.get(user=request.auth.user)

        plant = Plant.objects.create(
            user = helpLifeUser,
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


class HelpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpLifeUser
        fields = ("username", )

class CareTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareTip
        fields = ( "id",
            "plant_tip_label",
            "description_of_tip", 
        )

class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = (
            "id",
            "plant_type", 
        )

class PlantSerializer(serializers.ModelSerializer):

    user = HelpUserSerializer(many=False)
    care_tips = CareTipSerializer(many=True)
    plant_types = PlantTypeSerializer(many=True)

    class Meta:
        model = Plant
        fields = ('id', 
                'user', 
                'available', 
                'new_plant_care', 
                'plant_age', 
                'plant_name', 
                'plant_image', 
                'care_tips',
                'plant_types', )

