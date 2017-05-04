# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 19:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0048_remove_situation_first_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='situation',
            name='children',
            field=models.ManyToManyField(default=None, null=True, related_name='apostles', to='twep.MyTweet'),
        ),
        migrations.AddField(
            model_name='situation',
            name='first_tweet',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prophet', to='twep.MyTweet'),
        ),
    ]
