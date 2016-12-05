# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseLink', '0010_auto_20161205_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
