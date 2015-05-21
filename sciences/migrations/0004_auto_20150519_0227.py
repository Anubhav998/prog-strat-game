# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sciences', '0003_technologycost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technology',
            name='dependencies',
            field=models.ManyToManyField(to='sciences.Technology', blank=True),
        ),
    ]
