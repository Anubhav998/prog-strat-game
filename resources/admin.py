from django.contrib import admin

from reversion import VersionAdmin

from resources.models import Resource, ResourceCost


class ResourceCostInline(admin.TabularInline):
    model = ResourceCost
    fk_name = 'base'


@admin.register(Resource)
class ResourceAdmin(VersionAdmin):
    inlines = [ResourceCostInline]