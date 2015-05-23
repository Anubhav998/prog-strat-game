# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('combat', '0002_auto_20150523_0053'),
        ('matches', '0010_remove_territorystate_synced'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConflictState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('conflict', models.ForeignKey(to='combat.Conflict')),
                ('state', models.ForeignKey(related_name='conflicts', to='matches.GameState')),
            ],
        ),
    ]
