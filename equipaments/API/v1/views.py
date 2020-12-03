from collections import OrderedDict

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from equipaments.API.v1.serializers import (
    EquipamentSerializer,
    PatchEquipamenSerializer,
)
from equipaments.models import Equipament
from vessels.models import Vessel


class EquipamentView(APIView):
    """
    post:
    Create a new equipament instance.

    patch:
    Update equipament status by id. Receive one or a list of equipaments.

    """

    serializer_class = EquipamentSerializer

    def post(self, request):
        serializer = EquipamentSerializer(data=request.data or None)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data = request.data.copy()
        if isinstance(data["codes"], int):
            data["codes"] = [data["codes"]]
        serializer = PatchEquipamenSerializer(data=data, partial=True)
        if serializer.is_valid():
            for equipament_id in serializer.validated_data["codes"]:
                equipament = get_object_or_404(Equipament, pk=equipament_id)
                equipament.status = "INACTIVE"
                equipament.save()
            return Response({"Vessel(s) updated(s)"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListEquipamentsView(ListAPIView):
    """Return a list of all the existing equipaments by vessel."""

    serializer_class = EquipamentSerializer

    def get_queryset(self):
        vessel = self.request.query_params.get("vessel")
        vessel_code = get_object_or_404(Vessel, code=vessel)
        queryset = Equipament.objects.filter(vessel__code=vessel_code, status="Active")
        return queryset
