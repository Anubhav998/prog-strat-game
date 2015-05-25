import re

from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from core.models import AuditMixin
from core.matchers import COORDINATE_PAIR
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

    def get_by_coordinates(self, coordinates):
        """ Takes a string and returns the territory
        :param coordinates: a string of (x, y) of a territory
        :return: Territory Object
        """
        matches = re.match(COORDINATE_PAIR, coordinates)
        if not matches:
            raise ValidationError('invalid coordinate string')
        x, y = matches.groups()
        try:
            territory = self.territory_set.get(position_x=x, position_y=y)
        except ObjectDoesNotExist:
            raise ValidationError('no territory found at coordinates')
        return territory

    def check_coordinate(self, coordinate):
        """Takes a tuple of x,y and returns if it is on the arena"""
        x, y = coordinate
        return 0 <= x < self.size_x and 0 <= y < self.size_y


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

    def get_delta(self, delta):
        """Takes a move pair and returns coordinates"""
        dx, dy = delta
        return self.position_x + dx, self.position_y + dy

    def get_valid_moves(self):
        """Return 4 adjacent squares"""
        deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return [self.get_delta(delta) for delta in deltas if self.arena.check_coordinate(self.get_delta(delta))]


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
