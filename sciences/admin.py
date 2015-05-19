from django.contrib import admin

from sciences.models import Technology, ResourceBenefit, TechnologyCost


class ResourceBenefitInline(admin.TabularInline):
    model = ResourceBenefit


class TechnologyCostInline(admin.TabularInline):
    model = TechnologyCost


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    inlines = [ResourceBenefitInline, TechnologyCostInline]