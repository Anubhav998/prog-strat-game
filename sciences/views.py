import json

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_extensions.mixins import NestedViewSetMixin

from sciences.models import Technology, ResourceBenefit
from sciences.serializers import TechnologySerializer, ResourceBenefitSerializer
from resources.models import Resource


class TechnologyViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API Endpoints for Technologies
    """
    queryset = Technology.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = TechnologySerializer


class ResourceBenefitViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API Endpoints for resource benefits of a technology
    """
    queryset = ResourceBenefit.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ResourceBenefitSerializer

    def create(self, request, *args, **kwargs):
        post = request.POST or json.loads(request.body)
        resource_benefit = ResourceBenefit.objects.create(
            resource=Resource.objects.get(pk=post.get('resource')),
            technology=Technology.objects.get(pk=kwargs.get('parent_lookup_id')),
            modifier=post.get('modifier'),
            amount=post.get('amount')
        )
        serializer = ResourceBenefitSerializer(resource_benefit, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
