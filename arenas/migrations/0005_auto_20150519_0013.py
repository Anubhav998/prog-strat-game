# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('arenas', '0004_auto_20150519_0012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='territorydetail',
            name='costs',
        ),
        migrations.AddField(
            model_name='territorydetail',
            name='cost',
            field=models.PositiveIntegerField(default=500, blank=True),
        ),
    ]
