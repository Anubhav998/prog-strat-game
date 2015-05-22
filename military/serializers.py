from rest_framework import serializers

from military.models import Unit, Category, UnitCost, UnitDependency


class UnitDependencySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="technology.name")

    class Meta:
        model = UnitDependency
        fields = (
            'technology',
            'name',
        )


class UnitCostSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="resource.name")

    class Meta:
        model = UnitCost
        fields = (
            'resource',
            'name',
            'amount',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'description',
        )


class UnitSerializer(serializers.ModelSerializer):
    costs = UnitCostSerializer(many=True, read_only=True)
    dependencies = UnitDependencySerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = (
            'id',
            'name',
            'description',
            'category',
            'costs',
            'attack',
            'defence',
            'dependencies',
        )
