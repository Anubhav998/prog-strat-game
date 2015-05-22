from rest_framework import serializers
from rest_framework.reverse import reverse

from sciences.models import Technology, ResourceBenefit, TechnologyCost, TechnologyDependency


class TechnologyDependencySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='technology.name')

    class Meta:
        model = TechnologyDependency
        fields = (
            'technology',
            'name',
        )


class TechnologyCostSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='resource.name')

    class Meta:
        model = TechnologyCost
        fields = (
            'resource',
            'name',
            'amount',
        )


class ResourceBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceBenefit
        fields = (
            'resource',
            'modifier',
            'amount',
        )


class TechnologySerializer(serializers.ModelSerializer):
    benefits = ResourceBenefitSerializer(many=True, read_only=True)
    dependencies = TechnologyDependencySerializer(many=True, read_only=True)
    resources_url = serializers.SerializerMethodField()
    costs = TechnologyCostSerializer(many=True, read_only=True)

    class Meta:
        model = Technology
        fields = (
            'id',
            'name',
            'description',
            'dependencies',
            'costs',
            'benefits',
            'resources_url',
        )

    def get_resources_url(self, obj):
        return reverse('science-resources-list', args=(obj.id,), request=self.context.get('request'))
