from django.db import models

from reversion import register

from core.models import AuditMixin
from resources.models import Resource, Cost
from core.defaults import ARENA_X, ARENA_Y


@register
class Arena(AuditMixin):
    name = models.CharField(max_length=64)
    size_x = models.PositiveIntegerField(default=ARENA_X)
    size_y = models.PositiveIntegerField(default=ARENA_Y)

    def __unicode__(self):
        return self.name

    def get_size_display(self):
        return "{0.size_x}x{0.size_y}".format(self)


@register
class Territory(models.Model):
    arena = models.ForeignKey(Arena)
    position_x = models.PositiveIntegerField()
    position_y = models.PositiveIntegerField()

    def __unicode__(self):
        return "{0.arena.name} - ({1})".format(self, self.get_position_display())

    def get_position_display(self):
        return "{0.position_x},{0.position_y}".format(self)

    class Meta:
        unique_together = [('arena', 'position_x', 'position_y',)]


@register
class TerritoryDetail(models.Model):
    territory = models.OneToOneField(Territory)
    resources = models.ManyToManyField(Resource, through="TerritoryResource", blank=True)
    terrain = models.ForeignKey("Terrain", blank=True, null=True)

    def __unicode__(self):
        return "{0.territory} detail".format(self)


@register
class TerritoryResource(models.Model):
    territory_detail = models.ForeignKey(TerritoryDetail)
    resource = models.ForeignKey(Resource)
    amount = models.IntegerField()

    def __unicode__(self):
        return "{0.territory_detail.territory} {0.resource}".format(self)


@register
class TerritoryCosts(Cost):
    territory_detail = models.ForeignKey(TerritoryDetail, related_name='costs')


@register
class Terrain(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name