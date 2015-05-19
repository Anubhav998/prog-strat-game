import json

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_extensions.mixins import NestedViewSetMixin

from arenas.models import Arena, Terrain, TerritoryDetail, TerritoryResource
from arenas.serializers import ArenaSerializer, TerrainSerializer, TerritoryDetailSerializer
from resources.models import Resource


class ArenaViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API Endpoints for Arenas
    """
    queryset = Arena.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ArenaSerializer

    def create(self, request, *args, **kwargs):
        post = request.POST or json.loads(request.body)
        arena = Arena.objects.create(
            created_by=request.user,
            name=post.get('name', False),
            size_x=post.get('size_x', 16),
            size_y=post.get('size_y', 16)
        )
        serializer = ArenaSerializer(arena, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TerritoryDetailViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    API Endpoints for Territory Details
    """
    queryset = TerritoryDetail.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = TerritoryDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        detail = TerritoryDetail.objects.get(territory_id=kwargs.get('pk'))
        serializer = TerritoryDetailSerializer(detail, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        post = request.POST or json.loads(request.body)
        detail = TerritoryDetail.objects.get(territory_id=kwargs.get('pk'))
        if post.get('terrain', False):
            detail.terrain = Terrain.objects.get(pk=post.get('terrain'))
        if post.get('resources', False):
            detail.resources.clear()
            for resource_value in post.get('resources'):
                resource = Resource.objects.get(pk=resource_value.get('id'))
                value = resource_value.get('value')
                TerritoryResource.objects.create(
                    resource=resource,
                    territory_detail=detail,
                    amount=value
                )
        serializer = TerritoryDetailSerializer(detail, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TerrainViewSet(viewsets.ModelViewSet):
    """
    API Endpoints for Terrain
    """
    queryset = Terrain.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = TerrainSerializer