# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('arenas', '0002_auto_20150518_0357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='territorydetail',
            name='cost',
            field=models.PositiveIntegerField(default=500, blank=True),
        ),
        migrations.AlterField(
            model_name='territorydetail',
            name='resources',
            field=models.ManyToManyField(to='resources.Resource', through='arenas.TerritoryResource', blank=True),
        ),
    ]
