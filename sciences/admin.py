from django.contrib import admin

from sciences.models import Technology, ResourceBenefit


class ResourceBenefitInline(admin.TabularInline):
    model = ResourceBenefit


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    inlines = [ResourceBenefitInline]