from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_extensions.mixins import NestedViewSetMixin

from military.models import Unit, Category
from military.serializers import UnitSerializer, CategorySerializer


class UnitViewSet(viewsets.ModelViewSet):
    """
    API Endpoints for Technologies
    """
    queryset = Unit.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = UnitSerializer


class CategoryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API Endpoints for resource benefits of a technology
    """
    queryset = Category.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = CategorySerializer