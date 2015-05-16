from django.db import models


class Resource(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'resource'
        verbose_name_plural = 'resources'