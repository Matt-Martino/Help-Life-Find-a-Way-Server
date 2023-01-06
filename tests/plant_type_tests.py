import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from helplifeapi.models import HelpLifeUser, PlantType



class PlantTypeTests(APITestCase):

    fixtures = ['users', 'tokens', 'plant', 'care_tip', 'help_life_user', 'plant_type']

    def setUp(self):
        self.help_life_user = HelpLifeUser.objects.first()
        token = Token.objects.get(user=self.help_life_user.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_plant_type(self):
        """
        Ensure we can create a new plant type.
        """
        url = "/plantTypes"

        data = {
            "plant_type": "Tree2",
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["plant_type"], "Tree2")
        
        
    def test_get_plant_type(self):
        """
        Ensure we can get an existing plant type.
        """
        plant_type = PlantType()
        plant_type.plant_type = "This is an example type to test"
        plant_type.save()

        response = self.client.get(f"/plantTypes/{plant_type.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["plant_type"], "This is an example type to test")
        
    def test_change_plant_type(self):
        """
        Ensure we can change an existing plant type info.
        """
        plant_type = PlantType()
        plant_type.plant_type = "This is the test type"
        plant_type.save()

        data = {
            "plant_type": "this is the new",
        }

        response = self.client.put(f"/plantTypes/{plant_type.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/plantTypes/{plant_type.id}")
        json_response = json.loads(response.content)

        self.assertEqual(json_response["plant_type"], "this is the new")
        

    def test_delete_plant_type(self):
        """
        Ensure we can delete an existing plant type.
        """
        plant_type = PlantType()
        plant_type.id = 1
        plant_type.save()

        response = self.client.delete(f"/plantTypes/{plant_type.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/plantTypes/{plant_type.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)