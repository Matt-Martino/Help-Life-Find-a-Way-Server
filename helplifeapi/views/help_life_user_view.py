from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from helplifeapi.models import HelpLifeUser, Plant
from django.contrib.auth.models import User

class HelpLifeUserView(ViewSet):

    def retrieve(self, request, pk):

        help_life_user = HelpLifeUser.objects.get(pk=pk)
        serializer = HelpLifeUserSerializer(help_life_user)
        return Response(serializer.data)


    def list(self, request):
        help_life_users = HelpLifeUser.objects.all()
        plants = Plant.objects.all()

        plant_list = []
        for plant in plants:
            for help_life_user in help_life_users:
                if plant.user.id == help_life_user.id:
                    plant_list.append(plant)
                    help_life_user.plant_count = len(plant_list)

        serializer = HelpLifeUserSerializer(help_life_users, many=True)
        return Response(serializer.data)


    def update(self, request, pk):

        help_life_user = HelpLifeUser.objects.get(pk=pk)
        user = User.objects.get(pk=help_life_user.user_id)
        help_life_user.bio = request.data["bio"]
        help_life_user.profile_image_url = request.data["profile_image_url"]
        user.is_staff = request.data["is_staff"]
        user.is_active = request.data["is_active"]
        user.save()
        help_life_user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        help_life_user = HelpLifeUser.objects.get(pk=pk)
        help_life_user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "is_staff", "date_joined", "email", "is_active", )
        

class HelpLifeUserSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)
    class Meta:
        model = HelpLifeUser
        fields = ('id', 'user', "full_name", 'bio', 'profile_image_url', "tokenNumber", "plant_count", )
        