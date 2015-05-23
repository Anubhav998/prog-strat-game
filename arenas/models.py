from django.db import models
from django.core.exceptions import ValidationError

from core.models import AuditMixin
from resources.models import Resource, Cost
from core.defaults import ARENA_X, ARENA_Y, TERRITORY_ACQUISITION


class Arena(AuditMixin):
    name = models.CharField(max_length=64)
    size_x = models.PositiveIntegerField(default=ARENA_X)
    size_y = models.PositiveIntegerField(default=ARENA_Y)

    def __unicode__(self):
        return self.name

    def normalize(self, position):
        """Method to normalize a coordinate pair to a grid.
        will return the coordinates, converting negatives to positives

        :param position: tuple of (x, y), allowing negatives
        :return: x, y
        """
        x, y = position
        x = x if x >= 0 else self.size_x + x
        y = y if y >= 0 else self.size_y + y
        if x > (self.size_x - 1) or y > (self.size_y - 1):
            raise ValidationError('invalid coordinates')
        return x, y

    def get_size_display(self):
        return "{0.size_x}x{0.size_y}".format(self)


class Territory(models.Model):
    arena = models.ForeignKey(Arena)
    position_x = models.PositiveIntegerField()
    position_y = models.PositiveIntegerField()

    def __unicode__(self):
        return "{0.arena.name} - ({1})".format(self, self.get_position_display())

    def get_position_display(self):
        return "{0.position_x},{0.position_y}".format(self)

    def get_coordinates(self):
        return self.position_x, self.position_y

    class Meta:
        unique_together = [('arena', 'position_x', 'position_y',)]


class TerritoryDetail(models.Model):
    territory = models.OneToOneField(Territory)
    resources = models.ManyToManyField(Resource, through="TerritoryResource", blank=True)
    terrain = models.ForeignKey("Terrain", blank=True, null=True)
    acquisition = models.IntegerField(default=TERRITORY_ACQUISITION)

    def __unicode__(self):
        return "{0.territory} detail".format(self)


class TerritoryResource(models.Model):
    territory_detail = models.ForeignKey(TerritoryDetail, related_name='produces')
    resource = models.ForeignKey(Resource)
    amount = models.IntegerField()

    def __unicode__(self):
        return "{0.territory_detail.territory} {0.resource}".format(self)


class TerritoryCosts(Cost):
    territory_detail = models.ForeignKey(TerritoryDetail, related_name='costs')


class Terrain(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name
