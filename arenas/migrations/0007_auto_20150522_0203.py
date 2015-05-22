# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('arenas', '0006_auto_20150519_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='territoryresource',
            name='territory_detail',
            field=models.ForeignKey(related_name='produces', to='arenas.TerritoryDetail'),
        ),
    ]
