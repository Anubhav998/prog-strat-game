# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('sciences', '0004_auto_20150519_0227'),
        ('resources', '0008_auto_20150521_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resource', models.ForeignKey(related_name='dependencies', to='resources.Resource')),
                ('technology', models.ForeignKey(to='sciences.Technology')),
            ],
        ),
    ]
