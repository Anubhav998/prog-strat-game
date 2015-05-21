# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0003_auto_20150521_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReligionState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(default=0)),
                ('state', models.ForeignKey(related_name='religion', to='matches.GameState')),
            ],
        ),
    ]
