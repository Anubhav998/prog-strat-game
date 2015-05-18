from django.db import models

from core.models import AuditMix


class Arena(AuditMix):
    name = models.CharField(max_length=64)
    size_x = models.PositiveIntegerField(default=16)
    size_y = models.PositiveIntegerField(default=16)

    def __unicode__(self):
        return self.name

    def get_size_display(self):
        return "{0.size_x}x{0.size_y}".format(self)


class Territory(models.Model):
    arena = models.ForeignKey(Arena)
    position_x = models.PositiveIntegerField()
    position_y = models.PositiveIntegerField()

    def __unicode__(self):
        return "{0.arena.name} - ({0.get_position_display})".format(self)

    def get_position_display(self):
        return "{0.position_x},{0.position_y}"

    class Meta:
        unique_together = [('arena', 'position_x', 'position_y',)]

