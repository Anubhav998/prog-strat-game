# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sciences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcebenefit',
            name='modifier',
            field=models.CharField(default=b'+', max_length=1, choices=[(b'-', b'-'), (b'+', b'+'), (b'*', b'*'), (b'/', b'/')]),
        ),
    ]
