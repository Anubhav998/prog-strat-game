from django.contrib import admin

from arenas.models import Arena, Terrain


@admin.register(Arena)
class ArenaAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_size_display']


@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    pass