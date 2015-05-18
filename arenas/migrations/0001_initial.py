# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arena',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=64)),
                ('size_x', models.PositiveIntegerField(default=16)),
                ('size_y', models.PositiveIntegerField(default=16)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Territory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position_x', models.PositiveIntegerField()),
                ('position_y', models.PositiveIntegerField()),
                ('arena', models.ForeignKey(to='arenas.Arena')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='territory',
            unique_together=set([('arena', 'position_x', 'position_y')]),
        ),
    ]
