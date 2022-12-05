from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helplifeapi.models import PlantType

class PlantTypeView(ViewSet):
    """HelpLife Care Tip view"""

    def retrieve(self, request, pk):
        try: 
            plant_type = PlantType.objects.get(pk=pk)
        except PlantType.DoesNotExist:
            return Response({"message": "Care Tip does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = PlantTypeSerializer(plant_type)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        plant_types = PlantType.objects.all()
        serializer = PlantTypeSerializer(plant_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        plant_type = PlantType.objects.create(
            plant_type = request.data["plant_type"],
            )
        serializer = PlantTypeSerializer(plant_type)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        plant_type = PlantType.objects.get(pk=pk)
        plant_type.plant_type = request.data["plant_type"]
        plant_type.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        plant_type = PlantType.objects.get(pk=pk)
        plant_type.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PlantTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlantType
        fields = ('id', 'plant_type', )

