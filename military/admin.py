from django.contrib import admin

from military.models import Unit, UnitCost, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class UnitCostInline(admin.TabularInline):
    model = UnitCost


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    inlines = [UnitCostInline]