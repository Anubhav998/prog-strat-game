from django.contrib import admin

from reversion import VersionAdmin

from resources.models import Resource


@admin.register(Resource)
class ResourceAdmin(VersionAdmin):
    pass