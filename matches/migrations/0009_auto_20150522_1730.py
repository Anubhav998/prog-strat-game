# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0008_auto_20150522_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='territorystate',
            name='synced',
            field=models.IntegerField(default=0),
        ),
    ]
