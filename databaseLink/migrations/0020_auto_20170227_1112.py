# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-27 11:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databaseLink', '0019_auto_20170115_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='troop',
            name='isGuard',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelTable(
            name='lastsavedtimestamp',
            table='LastSavedTimeStamps',
        ),
    ]
