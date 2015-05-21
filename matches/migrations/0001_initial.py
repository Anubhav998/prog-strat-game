# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):
    dependencies = [
        ('sciences', '0004_auto_20150519_0227'),
        ('military', '0002_auto_20150519_0039'),
        ('resources', '0003_auto_20150519_0039'),
        ('arenas', '0006_auto_20150519_0039'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='GameState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player', models.IntegerField(blank=True, null=True,
                                               choices=[(0, b'Global'), (1, b'Player One'), (2, b'Player Two')])),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                (
                    'victor',
                    models.IntegerField(blank=True, null=True, choices=[(1, b'Player One'), (2, b'Player Two')])),
                ('arena', models.ForeignKey(to='arenas.Arena')),
                ('player_1', models.ForeignKey(related_name='player_one', to='profiles.Profile')),
                ('player_2', models.ForeignKey(related_name='player_two', to='profiles.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='MilitaryState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('state', models.ForeignKey(related_name='military', to='matches.GameState')),
                ('unit', models.ForeignKey(to='military.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=0)),
                ('action', models.ForeignKey(to='matches.Action')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('resource', models.ForeignKey(to='resources.Resource')),
                ('state', models.ForeignKey(related_name='resources', to='matches.GameState')),
            ],
        ),
        migrations.CreateModel(
            name='TechnologyState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('state', models.ForeignKey(related_name='technology', to='matches.GameState')),
                ('technology', models.ForeignKey(to='sciences.Technology')),
            ],
        ),
        migrations.CreateModel(
            name='TerritoryState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (
                    'player',
                    models.IntegerField(blank=True, null=True, choices=[(1, b'Player One'), (2, b'Player Two')])),
                ('status', models.CharField(max_length=64, choices=[(b'owned', b'Owned'), (b'valid', b'Valid'),
                                                                    (b'conflict', b'Conflict'), (b'open', b'Open')])),
                ('state', models.ForeignKey(related_name='territory', to='matches.GameState')),
                ('territory', models.ForeignKey(to='arenas.Territory')),
            ],
        ),
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('match', models.ForeignKey(related_name='turns', to='matches.Match')),
                ('profile', models.ForeignKey(to='profiles.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='move',
            name='turn',
            field=models.ForeignKey(related_name='moves', to='matches.Turn'),
        ),
        migrations.AddField(
            model_name='gamestate',
            name='match',
            field=models.ForeignKey(to='matches.Match'),
        ),
        migrations.AlterUniqueTogether(
            name='turn',
            unique_together=set([('match', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='match',
            unique_together=set([('player_1', 'player_2', 'uuid')]),
        ),
        migrations.AlterUniqueTogether(
            name='gamestate',
            unique_together=set([('match', 'player')]),
        ),
    ]
