# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
        ('arenas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terrain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='TerritoryDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TerritoryResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('resource', models.ForeignKey(to='resources.Resource')),
                ('territory_detail', models.ForeignKey(to='arenas.TerritoryDetail')),
            ],
        ),
        migrations.AddField(
            model_name='territorydetail',
            name='resources',
            field=models.ManyToManyField(to='resources.Resource', null=True, through='arenas.TerritoryResource', blank=True),
        ),
        migrations.AddField(
            model_name='territorydetail',
            name='terrain',
            field=models.ForeignKey(blank=True, to='arenas.Terrain', null=True),
        ),
        migrations.AddField(
            model_name='territorydetail',
            name='territory',
            field=models.OneToOneField(to='arenas.Territory'),
        ),
    ]
