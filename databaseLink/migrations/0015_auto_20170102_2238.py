# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-02 22:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databaseLink', '0014_remove_turnevent_realm'),
    ]

    operations = [
        migrations.AddField(
            model_name='realm',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='moveevent',
            name='troop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='databaseLink.Troop'),
        ),
        migrations.AlterField(
            model_name='turnorder',
            name='realm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Realm'),
        ),
    ]
