from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helplifeapi.models import UserPlantPlantType, PlantType, Plant


class UserPlantPlantTypeView(ViewSet):
    """User plant plant type view.  The join table between plants and plants"""

    def retrieve(self, request, pk):
        try: 
            user_plant_plant_type = UserPlantPlantType.objects.get(pk=pk)
        except UserPlantPlantType.DoesNotExist:
            return Response({"message": "user plant plant type does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = UserPlantPlantTypeSerializer(user_plant_plant_type)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        user_plant_plant_types = UserPlantPlantType.objects.all()
        if "plant" in request.query_params:
            query_value = request.query_params["plant"]
            user_plant_plant_types =user_plant_plant_types.filter(plant_id = query_value)
        serializer = UserPlantPlantTypeSerializer(user_plant_plant_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        plant_type_id = PlantType.objects.get(pk=request.data["plant_type"])
        plant_id = Plant.objects.get(pk=request.data["plant"])

        if UserPlantPlantType.objects.filter( plant_type_id=request.data["plant_type"], plant_id=request.data["plant"] ).exists():
            return Response("Data already exists", status=status.HTTP_409_CONFLICT)

        user_plant_plant_type = UserPlantPlantType.objects.create(
            plant_type = plant_type_id,
            plant = plant_id
            )

        serializer = UserPlantPlantTypeSerializer(user_plant_plant_type)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        user_plant_plant_type = UserPlantPlantType.objects.get(pk=pk)
        user_plant_plant_type.plant_type = request.data["plant_type"]
        user_plant_plant_type.plant = request.data["plant"]
        user_plant_plant_type.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        user_plant_plant_type = UserPlantPlantType.objects.get(pk=pk)
        user_plant_plant_type.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = ('id', 'plant_type', )

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ('id', 
                'user', 
                'available', 
                'new_plant_care', 
                'plant_age', 
                'plant_name', 
                'plant_image', )

class UserPlantPlantTypeSerializer(serializers.ModelSerializer):
    plant_type = PlantTypeSerializer(many=False)
    plant = PlantSerializer(many=False)

    class Meta:
        model = UserPlantPlantType
        fields = ('id', 'plant_type', 'plant', )
        depth = 1

