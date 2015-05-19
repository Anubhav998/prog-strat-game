from django.contrib import admin

from arenas.models import Arena, Terrain, TerritoryDetail, TerritoryCosts


class TerritoryCostAdmin(admin.TabularInline):
    model = TerritoryCosts


@admin.register(Arena)
class ArenaAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_size_display']


@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    pass


@admin.register(TerritoryDetail)
class TerrainDetailAdmin(admin.ModelAdmin):
    inlines = [TerritoryCostAdmin]