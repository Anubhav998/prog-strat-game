from django.contrib import admin

from reversion import VersionAdmin

from sciences.models import Technology, ResourceBenefit, TechnologyCost


class ResourceBenefitInline(admin.TabularInline):
    model = ResourceBenefit


class TechnologyCostInline(admin.TabularInline):
    model = TechnologyCost


@admin.register(Technology)
class TechnologyAdmin(VersionAdmin):
    inlines = [ResourceBenefitInline, TechnologyCostInline]