from django.db import models


class Resource(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'resource'
        verbose_name_plural = 'resources'


class Cost(models.Model):
    resource = models.ForeignKey(Resource)
    amount = models.PositiveIntegerField()

    def __unicode__(self):
        return "{0.amount} {0.resource}".format(self)

    class Meta:
        abstract = True


class ResourceCost(models.Model):
    resource = models.ForeignKey(Resource, related_name='costs')
    dependency = models.ForeignKey(Resource, related_name='dependency')
    amount = models.PositiveIntegerField()

    def __unicode__(self):
        return "{0.amount} {0.resource}".format(self)
