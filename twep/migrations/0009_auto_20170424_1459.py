# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0008_auto_20170424_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='tweets',
        ),
        migrations.AddField(
            model_name='keyword',
            name='tweets',
            field=models.ManyToManyField(default=None, null=True, to='twep.MyTweet'),
        ),
    ]