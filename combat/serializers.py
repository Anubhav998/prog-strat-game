from rest_framework import serializers

from combat.models import Conflict, AggressorUnit, DefenderUnit
from military.serializers import UnitSerializer
from arenas.serializers import TerritorySerializer


class AggressorUnitSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = AggressorUnit
        fields = (
            'unit',
        )


class DefenderUnitSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = DefenderUnit
        fields = (
            'unit',
        )


class ConflictSerializer(serializers.ModelSerializer):
    territory = TerritorySerializer(read_only=True)
    offence = AggressorUnitSerializer(many=True, read_only=True)
    defence = DefenderUnitSerializer(many=True, read_only=True)

    class Meta:
        model = Conflict
        fields = (
            'territory',
            'aggressor',
            'defender',
            'start_turn',
            'complete_turn',
            'complete',
            'victory',
            'offence',
            'defence',
        )
