from rest_framework import serializers

from resources.models import Resource, ResourceCost, ResourceDependency


class ResourceCostSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='resource.name')

    class Meta:
        model = ResourceCost
        fields = (
            'resource',
            'name',
            'amount',
        )


class ResourceDependencySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='technology.name')

    class Meta:
        model = ResourceDependency
        fields = (
            'technology',
            'name',
        )


class ResourceSerializer(serializers.ModelSerializer):
    dependencies = ResourceDependencySerializer(many=True, read_only=True)
    costs = ResourceCostSerializer(many=True, read_only=True)

    class Meta:
        model = Resource
        fields = (
            'id',
            'name',
            'description',
            'dependencies',
            'costs',
        )
