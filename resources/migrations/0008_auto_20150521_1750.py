# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0007_auto_20150521_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcecost',
            name='resource',
            field=models.ForeignKey(to='resources.Resource'),
        ),
    ]
