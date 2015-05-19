from django.contrib import admin

from reversion import VersionAdmin

from arenas.models import Arena, Terrain, TerritoryDetail, TerritoryCosts


class TerritoryCostAdmin(admin.TabularInline):
    model = TerritoryCosts


@admin.register(Arena)
class ArenaAdmin(VersionAdmin):
    list_display = ['name', 'get_size_display']


@admin.register(Terrain)
class TerrainAdmin(VersionAdmin):
    pass


@admin.register(TerritoryDetail)
class TerrainDetailAdmin(VersionAdmin):
    inlines = [TerritoryCostAdmin]