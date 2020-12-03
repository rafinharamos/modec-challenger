from django.urls import path

from vessels.API.v1.views import VesselView

app_name = "vessels"

urlpatterns = [
    path("create-vessel/", VesselView.as_view(), name="create-vessel"),
]
