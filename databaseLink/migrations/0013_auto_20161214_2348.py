# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-14 23:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databaseLink', '0012_auto_20161205_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='BattleEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('overrun', models.BooleanField(default=False)),
                ('processed', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BuildEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('type', models.IntegerField()),
                ('processed', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('type', models.IntegerField()),
                ('x', models.IntegerField(blank=True, null=True)),
                ('y', models.IntegerField(blank=True, null=True)),
                ('direction', models.CharField(blank=True, choices=[(b'nw', b'north-west'), (b'ne', b'north-east'), (b'e', b'east'), (b'se', b'south-east'), (b'sw', b'south-west'), (b'w', b'west')], max_length=2, null=True)),
                ('firstX', models.IntegerField(blank=True, null=True)),
                ('firstY', models.IntegerField(blank=True, null=True)),
                ('secondX', models.IntegerField(blank=True, null=True)),
                ('secondY', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=2000)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MoveEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('processed', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Realm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='RecruitmentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField(null=True)),
                ('y', models.IntegerField(null=True)),
                ('footmen', models.IntegerField()),
                ('horsemen', models.IntegerField()),
                ('leaders', models.IntegerField()),
                ('lkp', models.IntegerField()),
                ('skp', models.IntegerField()),
                ('ships', models.IntegerField()),
                ('lks', models.IntegerField()),
                ('sks', models.IntegerField()),
                ('processed', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TreasuryEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.IntegerField()),
                ('processed', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('realm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Realm')),
            ],
        ),
        migrations.CreateModel(
            name='Troop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('armyId', models.IntegerField()),
                ('count', models.IntegerField()),
                ('leaders', models.IntegerField()),
                ('mounts', models.IntegerField()),
                ('lkp', models.IntegerField()),
                ('skp', models.IntegerField()),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('realm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Realm')),
            ],
        ),
        migrations.CreateModel(
            name='TurnEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'st', b'start'), (b'fi', b'finished')], default=b'st', max_length=2)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('realm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Realm')),
            ],
        ),
        migrations.CreateModel(
            name='TurnOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turnNumber', models.IntegerField()),
                ('turnOrder', models.IntegerField()),
                ('realm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Realm')),
            ],
        ),
        migrations.RenameModel(
            old_name='Char',
            new_name='Character',
        ),
        migrations.RenameModel(
            old_name='Reichszugehoerigkeit',
            new_name='RealmMembership',
        ),
        migrations.RenameModel(
            old_name='Reichsgebiet',
            new_name='RealmTerritory',
        ),
        migrations.RenameModel(
            old_name='Fluesse',
            new_name='River',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.RemoveField(
            model_name='ruestgueter',
            name='reich',
        ),
        migrations.RemoveField(
            model_name='truppen',
            name='reich',
        ),
        migrations.DeleteModel(
            name='Zugreihenfolge',
        ),
        migrations.RemoveField(
            model_name='character',
            name='reich',
        ),
        migrations.RemoveField(
            model_name='realmterritory',
            name='reich',
        ),
        migrations.AlterField(
            model_name='realmmembership',
            name='reich',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Realm'),
        ),
        migrations.DeleteModel(
            name='Reich',
        ),
        migrations.DeleteModel(
            name='Ruestgueter',
        ),
        migrations.DeleteModel(
            name='Truppen',
        ),
        migrations.AddField(
            model_name='turnevent',
            name='turn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databaseLink.TurnOrder'),
        ),
        migrations.AddField(
            model_name='recruitmentevent',
            name='army',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Troop'),
        ),
        migrations.AddField(
            model_name='recruitmentevent',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Building'),
        ),
        migrations.AddField(
            model_name='moveevent',
            name='troop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Troop'),
        ),
        migrations.AddField(
            model_name='building',
            name='realm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Realm'),
        ),
        migrations.AddField(
            model_name='battleevent',
            name='participants',
            field=models.ManyToManyField(to='databaseLink.Troop'),
        ),
        migrations.AddField(
            model_name='character',
            name='realm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Realm'),
        ),
        migrations.AddField(
            model_name='realmterritory',
            name='realm',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='databaseLink.Realm'),
            preserve_default=False,
        ),
    ]