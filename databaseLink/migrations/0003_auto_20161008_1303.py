# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-08 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseLink', '0002_auto_20161004_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ruestgueter',
            name='directiom',
        ),
        migrations.AddField(
            model_name='ruestgueter',
            name='direction',
            field=models.CharField(blank=True, choices=[('nw', 'north-west'), ('ne', 'north-east'), ('e', 'east'), ('se', 'south-east'), ('sw', 'south-west'), ('w', 'west')], max_length=1, null=True),
        ),
    ]
