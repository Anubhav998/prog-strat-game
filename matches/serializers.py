from rest_framework import serializers

from matches.models import Match, GameState, ResourceState, MilitaryState, TechnologyState, TerritoryState, \
    ReligionState


class ResourceStateSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='resource.name')

    class Meta:
        model = ResourceState
        fields = (
            'resource',
            'name',
            'quantity',
        )


class MilitaryStateSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='unit.name')

    class Meta:
        model = MilitaryState
        fields = (
            'unit',
            'name',
            'quantity',
        )


class TechnologyStateSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='technology.name')

    class Meta:
        model = TechnologyState
        fields = (
            'technology',
            'name',
            'acquired',
        )


class TerritoryStateSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = TerritoryState
        fields = (
            'territory',
            'coordinates',
            'player',
            'status',
            'is_base',
        )

    def get_coordinates(self, obj):
        return str(obj.territory.get_coordinates())


class ReligionStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReligionState
        fields = (
            'amount',
        )


class GameStateSerializer(serializers.ModelSerializer):
    resources = ResourceStateSerializer(many=True, read_only=True)
    military = MilitaryStateSerializer(many=True, read_only=True)
    technology = TechnologyStateSerializer(many=True, read_only=True)
    territory = TerritoryStateSerializer(many=True, read_only=True)
    religion = ReligionStateSerializer(many=True, read_only=True)

    class Meta:
        model = GameState
        fields = (
            'player',
            'resources',
            'military',
            'technology',
            'territory',
            'religion',
        )


class MatchSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = (
            'arena',
            'player_1',
            'player_2',
            'timestamp',
            'uuid',
            'completed',
            'victor',
        )

    def get_uuid(self, obj):
        return obj.uuid
