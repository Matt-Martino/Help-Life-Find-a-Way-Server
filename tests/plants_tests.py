import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from helplifeapi.models import HelpLifeUser, Plant


class PlantTests(APITestCase):

    
    fixtures = ['users', 'tokens', 'plant', 'plant_type', 'help_life_user', 'care_tip']

    def setUp(self):
        self.help_life_user = HelpLifeUser.objects.first()
        token = Token.objects.get(user=self.help_life_user.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_plant(self):
        """
        Ensure we can create a new plant.
        """
        url = "/plants"

        data = {
            "available": False,
            "new_plant_care": "Water, light, love, n'dirt = needs.",
            "plant_age": "Seedling",
            "plant_name": "name of plant",
            "plant_image": "https://res.cloudinary.com/dm0vsswx2/image/upload/v1670957153/plant2_fofptf.png	",
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["available"], False)
        self.assertEqual(json_response["new_plant_care"], "Water, light, love, n'dirt = needs.")
        self.assertEqual(json_response["plant_age"], "Seedling")
        self.assertEqual(json_response["plant_name"], "name of plant")
        self.assertEqual(json_response["plant_image"], "https://res.cloudinary.com/dm0vsswx2/image/upload/v1670957153/plant2_fofptf.png	")
        
        

    def test_get_plant(self):
        """
        Ensure we can get an existing plant.
        """
        plant = Plant()
        plant.available = False
        plant.new_plant_care = "Water, light, love, n'dirt = needs."
        plant.plant_age = "Seedling"
        plant.plant_name = "name of plant"
        plant.plant_image = "https://res.cloudinary.com/dm0vsswx2/image/upload/v1670957153/plant2_fofptf.png	"
        plant.user_id = 1

        plant.save()

        response = self.client.get(f"/plants/{plant.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["available"], False)
        self.assertEqual(json_response["new_plant_care"], "Water, light, love, n'dirt = needs.")
        self.assertEqual(json_response["plant_age"], "Seedling")
        self.assertEqual(json_response["plant_name"], "name of plant")
        self.assertEqual(json_response["plant_image"], "https://res.cloudinary.com/dm0vsswx2/image/upload/v1670957153/plant2_fofptf.png	")



    def test_change_plant(self):
        """
        Ensure we can change an existing plant info.
        """
        plant = Plant()
        plant.available = False
        plant.new_plant_care = "Water, light, love, n'dirt = needs."
        plant.plant_age = "Seedling"
        plant.plant_name = "name of plant"
        plant.plant_image = "https://res.cloudinary.com/dm0vsswx2/image/upload/v1670957153/plant2_fofptf.png	"
        plant.user_id = 1

        plant.save()

        data = {
            "available": False,
            "new_plant_care": "Water, light, love, n'dirt = needs. Plus the edits",
            "plant_age": "Seedling Plus the edits",
            "plant_name": "name of plant Plus the edits",
            "plant_image": "https://res.cloudinary.com/dm0vsswx2/image/upload/v1670957153/plant2_fofptf.png	",
        }

        response = self.client.put(f"/plants/{plant.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/plants/{plant.id}")
        json_response = json.loads(response.content)

        self.assertEqual(json_response["available"], False)
        self.assertEqual(json_response["new_plant_care"], "Water, light, love, n'dirt = needs. Plus the edits")
        self.assertEqual(json_response["plant_age"], "Seedling Plus the edits")
        self.assertEqual(json_response["plant_name"], "name of plant Plus the edits")
        self.assertEqual(json_response["plant_image"], "https://res.cloudinary.com/dm0vsswx2/image/upload/v1670957153/plant2_fofptf.png	")



    def test_delete_plant(self):
        """
        Ensure we can delete an existing plant.
        """
        plant = Plant()
        plant.id = 1
        plant.available = False
        plant.new_plant_care = "Water, light, love, n'dirt = needs."
        plant.plant_age = "Seedling"
        plant.plant_name = "name of plant"
        plant.plant_image = "https://res.cloudinary.com/dm0vsswx2/image/upload/v1670957153/plant2_fofptf.png	"
        plant.user_id = 1

        response = self.client.delete(f"/plants/{plant.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/plants/{plant.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)