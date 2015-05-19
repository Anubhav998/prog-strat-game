from rest_framework import serializers

from resources.models import Resource, Cost


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = (
            'id',
            'name',
            'description',
        )


class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost
        fields = (
            'resource',
            'amount',
        )