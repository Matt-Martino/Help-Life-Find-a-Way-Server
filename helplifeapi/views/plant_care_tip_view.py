from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helplifeapi.models import PlantCareTip

class PlantCareTipView(ViewSet):
    """HelpLife Care Tip view"""

    def retrieve(self, request, pk):
        try: 
            plant_care_tip = PlantCareTip.objects.get(pk=pk)
        except PlantCareTip.DoesNotExist:
            return Response({"message": "Care Tip does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = PlantCareTipSerializer(plant_care_tip)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        plant_care_tips = PlantCareTip.objects.all()
        serializer = PlantCareTipSerializer(plant_care_tips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        plant_care_tip = PlantCareTip.objects.create(
            care_tip = request.data["care_tip"],
            plant = request.data["plant"]
            )
        serializer = PlantCareTipSerializer(plant_care_tip)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        plant_care_tip = PlantCareTip.objects.get(pk=pk)
        plant_care_tip.care_tip = request.data["care_tip"]
        plant_care_tip.plant = request.data["plant"]
        plant_care_tip.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        plant = PlantCareTip.objects.get(pk=pk)
        plant.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PlantCareTipSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlantCareTip
        fields = ('id', 
                'care_tip', 
                'plant',  )