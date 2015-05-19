from rest_framework import serializers

from matches.models import Match, GameState, ResourceState, MilitaryState, TechnologyState, TerritoryState


class ResourceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceState
        fields = (
            'resource',
            'quantity',
        )


class MilitaryStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilitaryState
        fields = (
            'unit',
            'quantity',
        )


class TechnologyStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnologyState
        fields = (
            'technology',
            'quantity',
        )


class TerritoryStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerritoryState
        fields = (
            'territory',
            'player',
            'status',
        )


class GameStateSerializer(serializers.ModelSerializer):
    resources = ResourceStateSerializer(many=True, read_only=True)
    military = MilitaryStateSerializer(many=True, read_only=True)
    technology = TechnologyStateSerializer(many=True, read_only=True)
    territory = TerritoryStateSerializer(many=True, read_only=True)

    class Meta:
        model = GameState
        fields = (
            'player',
            'resources',
            'military',
            'technology',
            'territory',
        )


class MatchSerializer(serializers.ModelSerializer):
    states = GameStateSerializer(many=True, read_only=True)

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
            'get_turn_count',
        )