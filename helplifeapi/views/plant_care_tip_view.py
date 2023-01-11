from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helplifeapi.models import PlantCareTip, Plant, CareTip

class PlantCareTipView(ViewSet):
    """plant care tip view. The join table between plants and care tips."""

    def retrieve(self, request, pk):
        try: 
            plant_care_tip = PlantCareTip.objects.get(pk=pk)
        except PlantCareTip.DoesNotExist:
            return Response({"message": "Care Tip does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = PlantCareTipSerializer(plant_care_tip)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):

        plant_care_tips = PlantCareTip.objects.all()
        if "plant" in request.query_params:
            query_value = request.query_params["plant"]
            plant_care_tips =plant_care_tips.filter(plant_id = query_value)
        serializer = PlantCareTipSerializer(plant_care_tips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        care_tip_id = CareTip.objects.get(pk=request.data["care_tip"])
        plant_id = Plant.objects.get(pk=request.data["plant"])

        if PlantCareTip.objects.filter( care_tip_id=request.data["care_tip"], plant_id=request.data["plant"] ).exists():
            return Response("", status=status.HTTP_208_ALREADY_REPORTED)
            
        plant_care_tip = PlantCareTip.objects.create(
            care_tip = care_tip_id,
            plant = plant_id
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

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ('id', 
                'plant_name', )

class CareTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareTip
        fields = ('id', 'plant_tip_label', 'description_of_tip', )

class PlantCareTipSerializer(serializers.ModelSerializer):
    care_tip = CareTipSerializer(many=False)
    plant = PlantSerializer(many=False)

    class Meta:
        model = PlantCareTip
        fields = ('id', 
                'care_tip', 
                'plant',  )