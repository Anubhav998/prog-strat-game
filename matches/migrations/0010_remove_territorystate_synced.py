# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0009_auto_20150522_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='territorystate',
            name='synced',
        ),
    ]
