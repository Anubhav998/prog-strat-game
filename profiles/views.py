from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import DjangoModelPermissions

from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API Endpoints for profiles
    """
    queryset = Profile.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ProfileSerializer
