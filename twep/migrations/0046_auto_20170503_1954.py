# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0045_auto_20170503_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='situation',
            name='children',
            field=models.ManyToManyField(default=None, null=True, related_name='children', to='twep.MyTweet'),
        ),
    ]
