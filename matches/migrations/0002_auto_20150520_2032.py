# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):
    dependencies = [
        ('profiles', '0001_initial'),
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('match', models.ForeignKey(to='matches.Match')),
                ('profile', models.ForeignKey(to='profiles.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='gamestate',
            name='profile',
            field=models.ForeignKey(to='profiles.Profile', null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='object',
            field=models.CharField(default=b'', max_length=64),
        ),
        migrations.AlterField(
            model_name='gamestate',
            name='match',
            field=models.ForeignKey(related_name='states', to='matches.Match'),
        ),
        migrations.AlterField(
            model_name='gamestate',
            name='player',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Player One'), (2, b'Player Two')]),
        ),
        migrations.AlterField(
            model_name='militarystate',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='resourcestate',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='technologystate',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='militarystate',
            unique_together=set([('state', 'unit')]),
        ),
        migrations.AlterUniqueTogether(
            name='resourcestate',
            unique_together=set([('state', 'resource')]),
        ),
        migrations.AlterUniqueTogether(
            name='technologystate',
            unique_together=set([('state', 'technology')]),
        ),
        migrations.AlterUniqueTogether(
            name='territorystate',
            unique_together=set([('state', 'territory')]),
        ),
        migrations.AlterUniqueTogether(
            name='token',
            unique_together=set([('match', 'profile')]),
        ),
    ]
