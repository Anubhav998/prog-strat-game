from django.db import models

from reversion import register

from core.defaults import ATTACK, DEFENCE
from resources.models import Cost


@register
class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


@register
class Unit(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    category = models.ForeignKey(Category)

    attack = models.IntegerField(default=ATTACK)
    defence = models.IntegerField(default=DEFENCE)

    def __unicode__(self):
        return self.name

    def get_power_display(self):
        return "({0.attack},{0.defence})".format(self)


@register
class UnitCost(Cost):
    unit = models.ForeignKey(Unit, related_name='costs')


@register
class UnitDependency(models.Model):
    unit = models.ForeignKey(Unit, related_name='dependencies')
    technology = models.ForeignKey('sciences.Technology')
