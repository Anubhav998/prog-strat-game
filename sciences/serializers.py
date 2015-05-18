from rest_framework import serializers
from rest_framework.reverse import reverse
from sciences.models import Technology, ResourceBenefit


class ResourceBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceBenefit
        fields = (
            'resource',
            'modifier',
            'amount',
        )


class TechnologySerializer(serializers.ModelSerializer):
    resourcebenefit_set = ResourceBenefitSerializer(many=True, read_only=True)
    resources_url = serializers.SerializerMethodField()

    class Meta:
        model = Technology
        fields = (
            'id',
            'name',
            'description',
            'dependencies',
            'resourcebenefit_set',
            'resources_url',
        )

    def get_resources_url(self, obj):
        return reverse('science-resources-list', args=(obj.id,), request=self.context.get('request'))
