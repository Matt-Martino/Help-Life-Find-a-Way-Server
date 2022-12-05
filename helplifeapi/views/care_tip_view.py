from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from helplifeapi.models import CareTip

class CareTipView(ViewSet):
    """HelpLife Care Tip view"""

    def retrieve(self, request, pk):
        try: 
            care_tip = CareTip.objects.get(pk=pk)
        except CareTip.DoesNotExist:
            return Response({"message": "Care Tip does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = CareTipSerializer(care_tip)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        care_tips = CareTip.objects.all()
        serializer = CareTipSerializer(care_tips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        care_tip = CareTip.objects.create(
            plant_tip_label = request.data["plant_tip_label"],
            description_of_tip = request.data["description_of_tip"]
            )
        serializer = CareTipSerializer(care_tip)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        care_tip = CareTip.objects.get(pk=pk)
        care_tip.plant_tip_label = request.data["plant_tip_label"]
        care_tip.description_of_tip = request.data["description_of_tip"]
        care_tip.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        care_tip = CareTip.objects.get(pk=pk)
        care_tip.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CareTipSerializer(serializers.ModelSerializer):

    class Meta:
        model = CareTip
        fields = ('id', 'plant_tip_label', 'description_of_tip', )

