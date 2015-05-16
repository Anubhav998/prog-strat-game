from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import DjangoModelPermissions

from resources.models import Resource
from resources.serializers import ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """
    API Endpoints for Patient Evaluations
    """
    queryset = Resource.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ResourceSerializer

