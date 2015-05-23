# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('arenas', '0007_auto_20150522_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='territorydetail',
            name='acquisition',
            field=models.IntegerField(default=50),
        ),
    ]
