from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vessels.API.v1.serializers import Vesselserializer


class VesselView(APIView):
    """
    post:
    Create a new vessel instance.
    """

    serializer_class = Vesselserializer

    def post(self, request):
        serializer = Vesselserializer(data=request.data or None)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(Response)
