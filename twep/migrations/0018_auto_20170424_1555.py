# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0017_auto_20170424_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mytweet',
            name='keywords',
        ),
        migrations.AddField(
            model_name='keyword',
            name='tweets',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='twep.MyTweet'),
        ),
    ]
