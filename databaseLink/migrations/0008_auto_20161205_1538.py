# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseLink', '0007_auto_20161204_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zugreihenfolge',
            name='subZug',
        ),
        migrations.AlterField(
            model_name='zugreihenfolge',
            name='reihenfolge',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
