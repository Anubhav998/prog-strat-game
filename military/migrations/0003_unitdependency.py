# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('sciences', '0004_auto_20150519_0227'),
        ('military', '0002_auto_20150519_0039'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('technology', models.ForeignKey(to='sciences.Technology')),
                ('unit', models.ForeignKey(related_name='dependencies', to='military.Unit')),
            ],
        ),
    ]
