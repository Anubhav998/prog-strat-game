# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0002_cost'),
        ('military', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField()),
                ('resource', models.ForeignKey(to='resources.Resource')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='unit',
            name='costs',
        ),
        migrations.AddField(
            model_name='unitcost',
            name='unit',
            field=models.ForeignKey(related_name='costs', to='military.Unit'),
        ),
    ]
