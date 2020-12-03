from django.db import models

from vessels.models import Vessel

STATUS_CHOICES = [
    ("ACTIVE", "Active"),
    ("INACTIVE", "Inactive"),
]


class Equipament(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")
    vessel = models.ForeignKey(Vessel, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.code
