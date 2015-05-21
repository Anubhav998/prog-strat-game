# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('matches', '0002_auto_20150520_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='territorystate',
            name='status',
            field=models.CharField(default=b'open', max_length=64,
                                   choices=[(b'owned', b'Owned'), (b'valid', b'Valid'), (b'conflict', b'Conflict'),
                                            (b'open', b'Open')]),
        ),
    ]
