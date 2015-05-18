import json

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import DjangoModelPermissions

from arenas.models import Arena
from arenas.serializers import ArenaSerializer


class ArenaViewSet(viewsets.ModelViewSet):
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