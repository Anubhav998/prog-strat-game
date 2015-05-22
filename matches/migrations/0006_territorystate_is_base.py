# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0005_auto_20150522_0348'),
    ]

    operations = [
        migrations.AddField(
            model_name='territorystate',
            name='is_base',
            field=models.BooleanField(default=False),
        ),
    ]
