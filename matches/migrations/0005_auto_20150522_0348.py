# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('matches', '0004_religionstate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technologystate',
            name='quantity',
        ),
        migrations.AddField(
            model_name='technologystate',
            name='acquired',
            field=models.BooleanField(default=False),
        ),
    ]
