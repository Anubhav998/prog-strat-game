# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0002_cost'),
        ('arenas', '0003_auto_20150518_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='territorydetail',
            name='cost',
        ),
        migrations.AddField(
            model_name='territorydetail',
            name='costs',
            field=models.ManyToManyField(to='resources.Cost', null=True, blank=True),
        ),
    ]
