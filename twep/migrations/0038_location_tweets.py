# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0037_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='tweets',
            field=models.ManyToManyField(default=None, to='twep.MyTweet'),
        ),
    ]