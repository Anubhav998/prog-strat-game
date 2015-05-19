# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0002_cost'),
        ('arenas', '0005_auto_20150519_0013'),
    ]

    operations = [
        migrations.CreateModel(
            name='TerritoryCosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField()),
                ('resource', models.ForeignKey(to='resources.Resource')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='territorydetail',
            name='cost',
        ),
        migrations.AddField(
            model_name='territorycosts',
            name='territory_detail',
            field=models.ForeignKey(related_name='costs', to='arenas.TerritoryDetail'),
        ),
    ]
