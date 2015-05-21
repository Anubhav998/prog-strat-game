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
    resources = ResourceStateSerializer(many=True)
    military = MilitaryStateSerializer(many=True)
    technology = TechnologyStateSerializer(many=True)
    territory = TerritoryStateSerializer(many=True)

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
