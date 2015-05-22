# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0007_territorystate_sycned'),
    ]

    operations = [
        migrations.RenameField(
            model_name='territorystate',
            old_name='sycned',
            new_name='synced',
        ),
    ]
