# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_auto_20150519_0039'),
        ('sciences', '0002_auto_20150519_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechnologyCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField()),
                ('resource', models.ForeignKey(to='resources.Resource')),
                ('technology', models.ForeignKey(related_name='costs', to='sciences.Technology')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
