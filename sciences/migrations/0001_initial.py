# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceBenefit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modifier', models.CharField(default=b'+', max_length=1,
                                              choices=[(b'-', b'-'), (b'+', b'-'), (b'*', b'*'), (b'/', b'/')])),
                ('amount', models.IntegerField()),
                ('resource', models.ForeignKey(to='resources.Resource')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True)),
                ('dependencies', models.ManyToManyField(to='sciences.Technology', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'technology',
                'verbose_name_plural': 'technologies',
            },
        ),
        migrations.AddField(
            model_name='resourcebenefit',
            name='technology',
            field=models.ForeignKey(to='sciences.Technology'),
        ),
    ]
