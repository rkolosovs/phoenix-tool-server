# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-15 15:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('databaseLink', '0018_lastsavedtimestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='realmmembership',
            old_name='reich',
            new_name='realm',
        ),
    ]
