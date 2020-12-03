from django.db import models


class Vessel(models.Model):
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.code
