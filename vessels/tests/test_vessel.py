import json
from rest_framework.test import APITestCase
from rest_framework import status
from vessels.API.v1.serializers import Vesselserializer
from vessels.models import Vessel


class VesselTestCase(APITestCase):
    def setUp(self):
        Vessel.objects.create(code="MV102")
        Vessel.objects.create(code="MV412")

    def test_registration_vessel(self):
        data = {"code": "MV104"}
        response = self.client.post("/vessel/create-vessel/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicated_vessel(self):
        data = {"code": "MV102"}
        response = self.client.post("/vessel/create-vessel/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            {"code": ["Vessel with this code already exists"]},
        )

    def test_with_lower_value(self):
        data = {"code": "MV1"}
        response = self.client.post("/vessel/create-vessel/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content), {"code": ["Code must contain 5 digits"]}
        )

    def test_with_higher_value(self):
        data = {"code": "MV10258"}
        response = self.client.post("/vessel/create-vessel/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content), {"code": ["Code must contain 5 digits"]}
        )


class VesselSerializerTestCase(APITestCase):
    def test_valid_vessel_serializer(self):
        self.valid_serializer_data = {"code": "MV110"}

        serializer = Vesselserializer(data=self.valid_serializer_data)
        assert serializer.is_valid()
        assert serializer.validated_data == self.valid_serializer_data
        assert serializer.data == self.valid_serializer_data
        assert serializer.errors == {}
