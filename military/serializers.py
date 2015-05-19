from rest_framework import serializers
from rest_framework.reverse import reverse

from military.models import Unit, Category, UnitCost


class UnitCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitCost
        fields = (
            'resource',
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
        )