# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0003_auto_20150519_0039'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField()),
                ('dependency', models.ForeignKey(related_name='dependency', to='resources.Resource')),
                ('resource', models.ForeignKey(related_name='costs', to='resources.Resource')),
            ],
        ),
    ]
