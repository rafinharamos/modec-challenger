from rest_framework import serializers
from vessels.models import Vessel


class Vesselserializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True)

    class Meta:
        model = Vessel
        fields = ("code",)

    def validate_code(self, value):
        vessel = Vessel.objects
        if vessel.filter(code=value).exists():
            raise serializers.ValidationError("Vessel with this code already exists")
        elif len(value) < 5 or len(value) > 5:
            raise serializers.ValidationError("Code must contain 5 digits")
        return value
