from django.urls import path

from equipaments.API.v1.views import EquipamentView, ListEquipamentsView

app_name = "equipaments"

urlpatterns = [
    path("", EquipamentView.as_view(), name="equipament"),
    path("list-equipament", ListEquipamentsView.as_view(), name="list-equipament"),
]
