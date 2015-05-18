from rest_framework import serializers

from sciences.models import Technology, ResourceBenefit


class ResourceBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceBenefit
        fields = (
            # 'resource',
            'modifier',
            'amount',
        )


class TechnologySerializer(serializers.ModelSerializer):
    resourcebenefit_set = ResourceBenefitSerializer(many=True, read_only=True)

    class Meta:
        model = Technology
        fields = (
            'id',
            'name',
            'description',
            'dependencies',
            'resourcebenefit_set',
        )