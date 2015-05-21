# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0005_auto_20150521_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcecost',
            name='base',
            field=models.ForeignKey(related_name='base', to='resources.Resource', null=True),
        ),
        migrations.AlterField(
            model_name='resourcecost',
            name='resource',
            field=models.ForeignKey(related_name='costs', to='resources.Resource'),
        ),
    ]
