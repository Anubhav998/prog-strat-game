from django.db import models

from core.defaults import ATTACK, DEFENCE
from resources.models import Cost


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    category = models.ForeignKey(Category)

    attack = models.IntegerField(default=ATTACK)
    defence = models.IntegerField(default=DEFENCE)

    def __unicode__(self):
        return self.name


class UnitCost(Cost):
    unit = models.ForeignKey(Unit, related_name='costs')
