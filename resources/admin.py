from django.contrib import admin

from reversion import VersionAdmin

from resources.models import Resource, ResourceCost, ResourceDependency


class ResourceCostInline(admin.TabularInline):
    model = ResourceCost
    fk_name = 'base'


class ResourceDependencyInline(admin.TabularInline):
    model = ResourceDependency


@admin.register(Resource)
class ResourceAdmin(VersionAdmin):
    inlines = [ResourceCostInline, ResourceDependencyInline]
