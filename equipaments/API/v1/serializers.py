from rest_framework import serializers
from equipaments import countries

from equipaments.models import Equipament
from vessels.models import Vessel


class EquipamentSerializer(serializers.ModelSerializer):
    vessel = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    class Meta:
        model = Equipament
        fields = ("code", "name", "location", "status", "vessel")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["vessel"] = instance.vessel.code
        return representation

    def validate_code(self, value):
        if Equipament.objects.filter(code=value).exists():
            raise serializers.ValidationError(
                "Equipament with this code already exists"
            )
        elif len(value) < 8 or len(value) > 8:
            raise serializers.ValidationError("Code must contain 8 digits")
        return value

    def validate_location(self, value):
        if value not in countries.countries.values():
            raise serializers.ValidationError("This countrie does not exist")
        return value

    def validate_vessel(self, value):
        try:
            obj = Vessel.objects.get(code=value)
            return obj

        except:
            raise serializers.ValidationError("Vessel does not exist")


class PatchEquipamenSerializer(serializers.ModelSerializer):
    codes = serializers.ListField(
        required=True,
        error_messages={
            "not_a_list": "Expected a list of items or a integer " "number(id)"
        },
    )

    class Meta:
        model = Equipament
        fields = ("codes",)

    def validate_codes(self, value):
        for id in value:
            if not isinstance(id, int):
                raise serializers.ValidationError("Only integer numbers are allowed")
            elif not Equipament.objects.filter(id=id).exists():
                raise serializers.ValidationError(f"The id {id} does not exists")

        return value
