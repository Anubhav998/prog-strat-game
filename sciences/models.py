from django.db import models

from resources.models import Cost


class Technology(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'technology'
        verbose_name_plural = 'technologies'


class TechnologyCost(Cost):
    technology = models.ForeignKey(Technology, related_name='costs')


class TechnologyDependency(models.Model):
    base = models.ForeignKey(Technology, related_name='dependencies')
    technology = models.ForeignKey(Technology)


class Benefit(models.Model):
    technology = models.ForeignKey(Technology, related_name='benefits')
    modifier = models.CharField(max_length=1, choices=(
        ('-', '-'),
        ('+', '+'),
        ('*', '*'),
        ('/', '/'),
    ), default="+")
    amount = models.IntegerField()

    def __unicode__(self):
        return "{0.modifier}{0.amount}".format(self)

    class Meta:
        abstract = True


class ResourceBenefit(Benefit):
    resource = models.ForeignKey("resources.Resource")

    def __unicode__(self):
        return "{0.technology} ({0.modifier}{0.amount} {0.resource.name})".format(self)
