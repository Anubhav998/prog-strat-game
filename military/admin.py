from django.contrib import admin

from military.models import Unit, UnitCost, Category, UnitDependency


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class UnitCostInline(admin.TabularInline):
    model = UnitCost


class UnitDependencyInline(admin.TabularInline):
    model = UnitDependency


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    inlines = [UnitCostInline, UnitDependencyInline]
