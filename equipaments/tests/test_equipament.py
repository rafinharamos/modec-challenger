import json

from rest_framework.test import APITestCase
from rest_framework import status

from equipaments.API.v1.serializers import (
    EquipamentSerializer,
)
from equipaments.models import Equipament
from vessels.models import Vessel


class EquipamentTestCase(APITestCase):
    def setUp(self):
        Vessel.objects.create(code="MV102")
        Vessel.objects.create(code="MV103")
        Vessel.objects.create(code="MV104")
        Vessel.objects.create(code="MV110")
        Equipament.objects.create(
            code="5310B9D1", name="compressor", location="Brazil", vessel_id=1
        )
        Equipament.objects.create(
            code="5310B9D2", name="extintor", location="Brazil", vessel_id=1
        )
        Equipament.objects.create(
            code="5310B9D3", name="bandeira", location="Brazil", vessel_id=2
        )
        Equipament.objects.create(
            code="5310B9D4", name="apito", location="Brazil", vessel_id=2
        )
        Equipament.objects.create(
            code="5310B9D5", name="lanterna", location="Brazil", vessel_id=3
        )
        Equipament.objects.create(
            code="5310B9D6", name="extintor", location="Brazil", vessel_id=3
        )

    def test_registration_equipament(self):
        data = {
            "code": "5310B9D7",
            "name": "compressor",
            "location": "Brazil",
            "vessel": "MV102",
        }
        response = self.client.post("/equipament/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_equipament_with_duplicated_code(self):
        data = {
            "code": "5310B9D1",
            "name": "compressor",
            "location": "Brazil",
            "vessel": "MV102",
        }
        response = self.client.post("/equipament/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {"code": ["Equipament with this code already exists"]},
        )

    def test_registration_with_lower_value(self):
        data = {
            "code": "531",
            "name": "compressor",
            "location": "Brazil",
            "vessel": "MV102",
        }
        response = self.client.post("/equipament/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content), {"code": ["Code must contain 8 digits"]}
        )

    def test_registration_with_higher_value(self):
        data = {
            "code": "53110B9D12587",
            "name": "compressor",
            "location": "Brazil",
            "vessel": "MV102",
        }
        response = self.client.post("/equipament/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content), {"code": ["Code must contain 8 digits"]}
        )

    def test_registration_equipament_with_inexistent_vessel(self):
        data = {
            "code": "5310B9D7",
            "name": "compressor",
            "location": "Brazil",
            "vessel": "MV140",
        }
        response = self.client.post("/equipament/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content), {"vessel": ["Vessel does not exist"]}
        )

    def test_registration_equipament_with_wrong_country(self):
        data = {
            "code": "5310B9D7",
            "name": "compressor",
            "location": "Invalid",
            "vessel": "MV102",
        }
        response = self.client.post("/equipament/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content), {"location": ["This countrie does not exist"]}
        )

    def test_list_equipaments(self):
        response = self.client.get("/equipament/list-equipament?vessel=MV102")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            [
                {
                    "code": "5310B9D1",
                    "name": "compressor",
                    "location": "Brazil",
                    "status": "Active",
                    "vessel": "MV102",
                },
                {
                    "code": "5310B9D2",
                    "name": "extintor",
                    "location": "Brazil",
                    "status": "Active",
                    "vessel": "MV102",
                },
            ],
        )

    def test_list_without_equipaments(self):
        response = self.client.get("/equipament/list-equipament?vessel=MV110")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), [])

    def test_list_with_no_vessel(self):
        response = self.client.get("/equipament/list-equipament?vessel=MV120")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})

    def test_patch_equipaments_one_element(self):
        data = {"codes": 1}
        response = self.client.patch("/equipament/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(json.loads(response.content), ["Vessel(s) updated(s)"])

    def test_patch_equipaments_list(self):
        data = {"codes": [1, 2, 3]}
        response = self.client.patch("/equipament/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(json.loads(response.content), ["Vessel(s) updated(s)"])

    def test_patch_id_word(self):
        data = {"codes": "a"}
        response = self.client.patch("/equipament/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {"codes": ["Expected a list of items or a integer number(id)"]},
        )

    def test_patch_inexistents_ids(self):
        data = {"codes": [44, 55, 66]}
        response = self.client.patch("/equipament/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content), {"codes": ["The id 44 does not exists"]}
        )


class EquipamentSerializerTestCase(APITestCase):
    def setUp(self):
        Vessel.objects.create(code="MV102")

    def test_valid_equipament_serializer(self):
        self.valid_serializer_data = {
            "code": "5310B9J7",
            "name": "compressor",
            "location": "Brazil",
            "vessel": "MV102",
        }

        serializer = EquipamentSerializer(data=self.valid_serializer_data)
        assert serializer.is_valid()
        assert serializer.errors == {}
