# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('sciences', '0004_auto_20150519_0227'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechnologyDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='technology',
            name='dependencies',
        ),
        migrations.AddField(
            model_name='technologydependency',
            name='base',
            field=models.ForeignKey(related_name='dependencies', to='sciences.Technology'),
        ),
        migrations.AddField(
            model_name='technologydependency',
            name='technology',
            field=models.ForeignKey(to='sciences.Technology'),
        ),
    ]
