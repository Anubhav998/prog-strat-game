from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import DjangoModelPermissions

from sciences.models import Technology
from sciences.serializers import TechnologySerializer


class TechnologyViewSet(viewsets.ModelViewSet):
    """
    API Endpoints for Resources
    """
    queryset = Technology.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = TechnologySerializer

