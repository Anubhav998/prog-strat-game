# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('profiles', '0001_initial'),
        ('military', '0003_unitdependency'),
        ('arenas', '0007_auto_20150522_0203'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggressorUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conflict',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_turn', models.IntegerField()),
                ('complete_turn', models.IntegerField(blank=True)),
                ('complete', models.BooleanField(default=False)),
                ('victory', models.NullBooleanField()),
                ('aggressor', models.ForeignKey(related_name='invasions', to='profiles.Profile')),
                ('defender', models.ForeignKey(related_name='defenses', blank=True, to='profiles.Profile', null=True)),
                ('territory', models.ForeignKey(to='arenas.Territory')),
            ],
        ),
        migrations.CreateModel(
            name='DefenderUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('conflict', models.ForeignKey(to='combat.Conflict')),
                ('unit', models.ForeignKey(to='military.Unit')),
            ],
        ),
        migrations.AddField(
            model_name='aggressorunit',
            name='conflict',
            field=models.ForeignKey(to='combat.Conflict'),
        ),
        migrations.AddField(
            model_name='aggressorunit',
            name='unit',
            field=models.ForeignKey(to='military.Unit'),
        ),
    ]
