# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0027_auto_20170427_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='tweets',
            field=models.ManyToManyField(default=None, to='twep.MyTweet'),
        ),
    ]
