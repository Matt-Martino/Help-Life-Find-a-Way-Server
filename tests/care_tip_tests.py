import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from helplifeapi.models import HelpLifeUser, CareTip


class CareTipTests(APITestCase):

    
    fixtures = ['users', 'tokens', 'plant', 'plant_type', 'help_life_user', 'care_tip']

    def setUp(self):
        self.help_life_user = HelpLifeUser.objects.first()
        token = Token.objects.get(user=self.help_life_user.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_care_tip(self):
        """
        Ensure we can create a new care tip.
        """
        url = "/careTips"

        data = {
            "plant_tip_label": "This is the plant care tip label",
            "description_of_tip": "A good description of the tip is here"
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["plant_tip_label"], "This is the plant care tip label")
        self.assertEqual(json_response["description_of_tip"], "A good description of the tip is here")



    def test_get_care_tip(self):
        """
        Ensure we can get an existing care tip.
        """
        care_tip = CareTip()
        care_tip.plant_tip_label = "This is the test tip name"
        care_tip.description_of_tip = "A good description of the tip is here"
        care_tip.save()

        response = self.client.get(f"/careTips/{care_tip.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["plant_tip_label"], "This is the test tip name")
        self.assertEqual(json_response["description_of_tip"], "A good description of the tip is here")


    def test_change_care_tip(self):
        """
        Ensure we can change an existing care tip info.
        """
        care_tip = CareTip()
        care_tip.plant_tip_label = "This is the test tip name"
        care_tip.description_of_tip = "A good description of the tip is here"
        care_tip.save()

        data = {
            "plant_tip_label": "this is the new label",
            "description_of_tip": "this is the other new thing we're doing"
        }

        response = self.client.put(f"/careTips/{care_tip.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/careTips/{care_tip.id}")
        json_response = json.loads(response.content)

        self.assertEqual(json_response["plant_tip_label"], "this is the new label")
        self.assertEqual(json_response["description_of_tip"], "this is the other new thing we're doing")


    def test_delete_care_tip(self):
        """
        Ensure we can delete an existing care tip.
        """
        care_tip = CareTip()
        care_tip.id = 1
        care_tip.save()

        response = self.client.delete(f"/careTips/{care_tip.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/careTips/{care_tip.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)