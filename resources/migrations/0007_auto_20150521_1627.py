# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0006_auto_20150521_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcecost',
            name='base',
            field=models.ForeignKey(related_name='costs', to='resources.Resource', null=True),
        ),
        migrations.AlterField(
            model_name='resourcecost',
            name='resource',
            field=models.ForeignKey(related_name='dependency', to='resources.Resource'),
        ),
    ]
