# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0011_conflictstate'),
    ]

    operations = [
        migrations.AddField(
            model_name='move',
            name='detail',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
