# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('combat', '0002_auto_20150523_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggressorunit',
            name='conflict',
            field=models.ForeignKey(related_name='offence', to='combat.Conflict'),
        ),
        migrations.AlterField(
            model_name='defenderunit',
            name='conflict',
            field=models.ForeignKey(related_name='defence', to='combat.Conflict'),
        ),
    ]
