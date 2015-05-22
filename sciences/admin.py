from django.contrib import admin

from reversion import VersionAdmin

from sciences.models import Technology, ResourceBenefit, TechnologyCost, TechnologyDependency


class ResourceBenefitInline(admin.TabularInline):
    model = ResourceBenefit


class TechnologyDependencyInline(admin.TabularInline):
    model = TechnologyDependency
    fk_name = 'base'


class TechnologyCostInline(admin.TabularInline):
    model = TechnologyCost


@admin.register(Technology)
class TechnologyAdmin(VersionAdmin):
    inlines = [ResourceBenefitInline, TechnologyCostInline, TechnologyDependencyInline]
