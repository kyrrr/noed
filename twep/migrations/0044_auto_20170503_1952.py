# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 19:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0043_situation_first_tweet_children'),
    ]

    operations = [
        migrations.AlterField(
            model_name='situation',
            name='first_tweet_children',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_tweet_children', to='twep.MyTweet'),
        ),
    ]
