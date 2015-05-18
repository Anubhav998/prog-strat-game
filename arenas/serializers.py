from rest_framework import serializers

from arenas.models import Arena, Territory


class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Territory
        fields = (
            'position_x',
            'position_y',
        )


class ArenaSerializer(serializers.ModelSerializer):
    territories = TerritorySerializer(source='territory_set', many=True, read_only=True)

    class Meta:
        model = Arena
        fields = (
            'id',
            'name',
            'territories',
            'size_x',
            'size_y'
        )