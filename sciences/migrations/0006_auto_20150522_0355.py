# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('sciences', '0005_auto_20150522_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcebenefit',
            name='technology',
            field=models.ForeignKey(related_name='benefits', to='sciences.Technology'),
        ),
    ]
