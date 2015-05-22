# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0006_territorystate_is_base'),
    ]

    operations = [
        migrations.AddField(
            model_name='territorystate',
            name='sycned',
            field=models.BooleanField(default=False),
        ),
    ]
