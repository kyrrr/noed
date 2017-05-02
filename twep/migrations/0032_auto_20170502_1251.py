# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 12:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twep', '0031_auto_20170502_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='situation',
            name='children',
        ),
        migrations.AddField(
            model_name='mytweet',
            name='situation_children',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='twep.Situation'),
        ),
    ]
