# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('military', '0002_auto_20150519_0039'),
        ('resources', '0002_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cost',
            name='resource',
        ),
        migrations.DeleteModel(
            name='Cost',
        ),
    ]
